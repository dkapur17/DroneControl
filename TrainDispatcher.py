# Train dispatcher script for easier training on ADA

import argparse
import json
import os
import tempfile

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

script = script.replace("{outputFile}", f"jobOutputs/{experimentName}_train_output.txt")
script = script.replace("{jobName}", f"{experimentName}_train")
script = script.replace("{configFile}", envConfig)
script = script.replace("{outputModelName}", modelName)

tmp = tempfile.NamedTemporaryFile()

with open(tmp.name, 'w') as f:
    f.write(script)

print(f"Dispatching Train Job for {experimentName}")

os.system(f"sbatch {tmp.name}")