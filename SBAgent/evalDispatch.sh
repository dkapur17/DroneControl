#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -o ../jobOutputs/bivariate_model2_output.txt
#SBATCH --job-name=bivariate_model2

python ParallelEvaluationPipeline.py models/base/model2/best_model.zip bivariate -t 1000 > model2_bivariate.md