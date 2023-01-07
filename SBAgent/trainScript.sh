#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH -o output_v6_lpf_0.1_at=4_18.txt
#SBATCH --job-name=v6_lpf_0.1_at=4_18

python TrainModel.py
