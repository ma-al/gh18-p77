
import os.path as osp
import os
import pandas as pd

def loadPopulationCSV():
	path = 'raw/Population-projections-ACT.csv'
	path = osp.normpath(osp.abspath(path))

	assert osp.isfile(path), path

	df = pd.read_csv(path)
	return df

def test():
    return 'test test gh18-p77'
