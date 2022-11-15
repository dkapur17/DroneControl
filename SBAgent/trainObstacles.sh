#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --mail-type=END,FAIL
#SBATCH -o output.txt
#SBATCH --exclude=gnode[001-054]
#SBATCH --job-name=train_target_10000000_steps

python TrainObstacles.py
