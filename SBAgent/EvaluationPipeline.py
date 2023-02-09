import os
import sys
import argparse
from tabulate import tabulate
from EvaluateModel import evaluate

parser = argparse.ArgumentParser()
parser.add_argument("modelPath", help="Path to the Model", type=str)
parser.add_argument("-t", "--trials", type=int, default=1000, help="Number of episodes to evaluate the model for in each environment.")
args = parser.parse_args()

mus = [0.0, 0.05, 0.1]
sigmas = [0.0, 0.1, 0.5, 1.0]
denoisers = ['None', 'LPF', 'KF']


print("# Evaluation Results")
print(f"**Model**: `{args.modelPath}`")
for mu in mus:
    for sigma in sigmas:
        for denoiser in denoisers:
            print(f"### $\mu = {mu}$ | $\sigma = {sigma}$ | Denoiser = `{denoiser}`\n")
            print(f"Evaluating {mu, sigma, denoiser}", file=sys.stderr)
            evaluationTable = evaluate(mu, sigma, denoiser.lower(), args.modelPath, args.trials, False, True)
            print(file=sys.stderr)
            print(tabulate(evaluationTable, headers=["Metric", "Value"], tablefmt='github'))
            print("---\n")
