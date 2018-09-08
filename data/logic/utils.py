
import os.path as osp
import os
import pandas as pd

normabs = lambda x: osp.normpath(osp.abspath(x))

def loadPopulationCSV(path):
	path = normabs(path)
	assert osp.isfile(path), path

	df = pd.read_csv(path)
	return df

def loadExcel(path):
	path = normabs(path)
	assert osp.isfile(path), path

	df = pd.read_excel(path)
	return df

def test():
    return 'test test gh18-p77'
