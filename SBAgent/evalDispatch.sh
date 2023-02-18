#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH -o ../jobOutputs/multivariate_model1_output.txt
#SBATCH --job-name=multivariate_model1

python ParallelEvaluationPipeline.py models/base/model1/best_model.zip multivariate -t 1000 > model1_multivariate.md