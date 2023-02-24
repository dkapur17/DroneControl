#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -o ../jobOutputs/model3_biased_output.txt
#SBATCH --job-name=model3_biased

python ParallelEvaluationPipeline.py models/base/model3/best_model.zip -t 1000 > model3_biased.md
