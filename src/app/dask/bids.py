import glob
import os
import time

import dask
from dask.distributed import Client

from ..commons.bids import run_group, run_participant, site_crawler, subject_crawler
from ..utils import load, merge_logs


def run(
    input_folder: str,
    output_folder: str,
    scheduler: str,
    benchmark: bool,
    container_path: str,
) -> None:
    experiment = f"dask:bids"
    start_time = time.time()
    common_args = {
        "benchmark": benchmark,
        "start": start_time,
        "input_folder": input_folder,
        "output_folder": output_folder,
        "experiment": experiment,
        "container_path": container_path,
    }

    client = Client(scheduler)

    subjects = subject_crawler(input_folder)
    sites = site_crawler(input_folder)

    for site in sites:
        site_folder = os.path.join(output_folder, site)
        if not os.path.exists(site_folder):
            os.mkdir(site_folder)

    futures = client.compute(
        [
            dask.delayed(run_participant)(
                subject_id=subject[1], site=subject[0], **common_args
            )
            for subject in subjects
        ]
    )
    client.gather(futures)
    futures = client.compute(
        [dask.delayed(run_group)(site=site, **common_args) for site in sites]
    )
    client.gather(futures)
    client.close()
    merge_logs(
        output_folder=output_folder,
        experiment=experiment,
    )