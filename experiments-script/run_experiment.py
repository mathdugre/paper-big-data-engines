import subprocess
from random import shuffle
import json


with open("experiment.json") as f_in:
    experiments = json.load(f_in)
    shuffle(experiments)
    for exp in experiments:
        experiment = exp["experiment"]
        filename = exp["file"]
        iterations = str(exp["iterations"])
        delay = str(exp["delay"])
        chunks = str(exp["chunks"])

        subprocess.run(
            ["sh", "/nfs/SOEN-499-Project/experiments-script/clear-cache.sh"]
        )

        if experiment[:5] == "spark":
            subprocess.run(
                [
                    "spark-submit",
                    "--master",
                    "spark://192.168.73.10:7077",
                    "--executor-memory",
                    "25G",
                    "/nfs/SOEN-499-Project/incrementation/" + filename,
                    "/nfs/bb-" + chunks + "chunks",
                    "/nfs/results",
                    experiment,
                    iterations,
                    delay,
                    "--benchmark",
                ]
            )
        else:
            subprocess.run(
                [
                    "python",
                    "/nfs/SOEN-499-Project/incrementation/" + filename,
                    "192.168.73.10:8786",
                    "/nfs/bb-" + chunks + "chunks",
                    "/nfs/results",
                    experiment,
                    iterations,
                    delay,
                    "--benchmark",
                ]
            )