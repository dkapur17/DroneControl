import re
import numpy as np
from typing import Union
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class EvalSummary:
    successRate: float
    failureRate: float
    meanIncompletionDistance: Union[float, None]
    meanReward: float
    meanEpisodeDuration: float

class AnalysisParser:

    def __init__(self):
        pass

    def parseAnalysisData(self, filePath):
        with open(filePath) as f:
            lines = f.readlines()

        self.content = ''.join(lines)
        self.chunks = self.getChunks()
        self.analysisData = self.parseChunks()
        return self.analysisData

    def getChunks(self):
        starts = [i.span()[0] for i in re.finditer(r'### ', self.content)]
        ends = [i.span()[0] for i in re.finditer(r'---\n', self.content)]
        chunks = [self.content[s:e] for (s,e) in zip(starts, ends)]
        return chunks

    def extractTitle(self, chunk):
        return re.findall(r'^### (.*)\n', chunk)[0]

    def parseTitle(self, title):
        mu = float(re.findall(r'\$\\mu = (.+?)\$', title)[0])
        sigma = float(re.findall(r'\$\\sigma = (.+?)\$', title)[0])
        denoiser = re.findall(r'Denoiser = `(.+)`', title)[0]
        return mu, sigma, denoiser

    def extractTable(self, chunk):
        table = re.findall(r'(\|(?:.+?)\|(?:.+?)\|\n)', chunk)
        return ''.join(table)

    def parseTable(self, table):
        lines = table.split('\n')
        # data = {}
        values = []
        for line in lines[2:-1]:
            cols = re.findall(r'\|.+\|', line)[0][1:-1].split('|')
            cols = [x.strip() for x in cols]
            metric, val = cols
            if val[-1] == '%':
                val = float(val[:-1])/100
            elif val == 'N/A':
                val = np.nan
            elif val[-1] == 'm':
                val = float(val[:-1])
            else:
                val = float(val)
            
            values.append(val)

        data = EvalSummary(*values)
        return data

    def parseChunks(self):
        
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        for chunk in self.chunks:
            title = self.extractTitle(chunk)
            mu, sigma, denoiser = self.parseTitle(title)
            table = self.extractTable(chunk)
            tableData = self.parseTable(table)
            data[mu][sigma][denoiser] = tableData
        
        return data