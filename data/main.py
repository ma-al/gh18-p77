
from logic import utils
from argparse import Namespace
import yaml


if __name__ == '__main__':
	print('test')
	print(utils.test())

	df = utils.loadPopulationCSV()
	print(df.head())

	path = utils.normabs('raw/example.yml')
	with open(path, 'r') as f:
		y = yaml.load(f)

	print('\n' * 4)
	print(y)

	print('\n' * 4)
	for postcode, data in y.items():
		print()
		print(f'postcode: {postcode}') 

		years = data['by_year']
		for year in years:
			ns = Namespace(**year)
			print(f'- {ns.year} = {ns.aged_pct}')