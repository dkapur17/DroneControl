#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -o ../jobOutputs/multivariate_model4_output.txt
#SBATCH --job-name=multivariate_model4

python ParallelEvaluationPipeline.py models/base/model4/best_model.zip multivariate -t 1000 > model4_multivariate.md