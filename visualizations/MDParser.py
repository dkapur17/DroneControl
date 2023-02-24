import re
import numpy as np

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
        mu = np.round(float(re.findall(r'\$\\mu = (.+?)\$', title)[0]), 3)
        sigma = np.round(float(re.findall(r'\$\\sigma = (.+?)\$', title)[0]), 3)
        denoiser = re.findall(r'Denoiser = `(.+)`', title)[0]
        return mu, sigma, denoiser

    def extractTable(self, chunk):
        table = re.findall(r'(\|(?:.+?)\|(?:.+?)\|\n)', chunk)
        return ''.join(table)

    def parseTable(self, table):
        lines = table.split('\n')
        data = {}

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
            
            data[metric] = val
        return data

    def parseChunks(self):
        
        data = {}
        for chunk in self.chunks:
            title = self.extractTitle(chunk)
            mu, sigma, denoiser = self.parseTitle(title)
            table = self.extractTable(chunk)
            tableData = self.parseTable(table)
            if mu not in data:
                data[mu] = {}
            if sigma not in data[mu]:
                data[mu][sigma] = {}
            if denoiser not in data[mu][sigma]:
                data[mu][sigma][denoiser] = {}
            data[mu][sigma][denoiser] = tableData
        
        return data