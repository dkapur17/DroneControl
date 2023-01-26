# Train dispatcher script for easier training on ADA

import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("experimentConfigFile", help="Experiment Config File Path")
args = parser.parse_args()

with open('trainScriptTemplate.sh', 'r') as f:
    script = ''.join(f.readlines())

with open(args.experimentConfigFile, 'r') as f:
    experimentConfig = json.load(f)

experimentName = experimentConfig["name"]
envConfig = experimentConfig["trainParameters"]["config"]
modelName = experimentConfig["trainParameters"]["outputModelName"]

jobOutputFile = os.path.join("jobOutputs", f"{modelName}_output.txt")

script = script.replace("{outputFileName}", jobOutputFile)
script = script.replace("{jobName}", experimentName)
script = script.replace("{configFile}", envConfig)
script = script.replace("{outputModelName}", modelName)

print(f"Dispatching Train Job for {experimentName}")

os.system(f"echo {script} | sbatch /dev/stdin")