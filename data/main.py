
from logic import utils



if __name__ == '__main__':
	print('test')
	print(utils.test())

	df = utils.loadPopulationCSV()
	print(df.head())