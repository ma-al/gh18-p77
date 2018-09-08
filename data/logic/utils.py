
import os.path as osp
import os
import pandas as pd

normabs = lambda x: osp.normpath(osp.abspath(x))

def loadPopulationCSV():
	path = normabs('raw/Population-projections-ACT.csv')
	assert osp.isfile(path), path

	df = pd.read_csv(path)
	return df

def test():
    return 'test test gh18-p77'
