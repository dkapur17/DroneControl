#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH -o {outputFile}
#SBATCH --job-name={jobName}

cd SBAgent
python TrainModel.py {configFile} {outputModelName} --steps {steps}