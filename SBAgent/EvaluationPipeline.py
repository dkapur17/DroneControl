import sys
import argparse
import numpy as np
import time
import datetime
from tabulate import tabulate
from EvaluateModel import evaluate

parser = argparse.ArgumentParser()
parser.add_argument("modelPath", help="Path to the Model", type=str)
parser.add_argument("method", choices={'bivariate', 'multivariate'}, help='Whether to perform bivariate or multivariate analysis', type=str)
parser.add_argument("-t", "--trials", type=int, default=1000, help="Number of episodes to evaluate the model for in each environment.")
args = parser.parse_args()


# Bivariate Parameters

if args.method == "bivariate":
    mus = np.arange(0, 0.21, 0.01)
    sigmas = np.arange(0, 2.1, 0.1)
    denoisers = ['None']
    print("# Bivariate Analysis")

else:
    mus = [0.0, 0.05, 0.1]
    sigmas = [0.0, 0.1, 0.5, 1.0]
    denoisers = ['None', 'LPF', 'KF']
    print("# Multivariate Analysis")

print(f"**Model**: `{args.modelPath}`")
for mu in mus:
    for sigma in sigmas:
        for denoiser in denoisers:
            print(f"### $\mu = {mu}$ | $\sigma = {sigma}$ | Denoiser = `{denoiser}`\n")
            print(f"Evaluating {mu, sigma, denoiser}", file=sys.stderr)
            startTime = time.time()
            evaluationTable = evaluate(mu, sigma, denoiser.lower(), args.modelPath, args.trials, False)
            endTime = time.time()
            print(file=sys.stderr)
            print(f"Time Taken: {datetime.timedelta(seconds=endTime-startTime)}", file=sys.stderr)
            print(tabulate(evaluationTable, headers=["Metric", "Value"], tablefmt='github'))
            print("---\n")
