#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH -o ../jobOutputs/multivariate_model2_output.txt
#SBATCH --job-name=multivariate_model2

python EvaluationPipeline.py models/base/model2/best_model.zip multivariate -t 1000 > model2_multivariate.md