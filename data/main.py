
from logic import utils
from argparse import Namespace
from collections import OrderedDict
import yaml

# from https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
def representOrderedDict(dumper, data):
    value = [(dumper.represent_data(k), dumper.represent_data(v)) for k, v in data.items()]
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, representOrderedDict)


def testCode():
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

def space(lines=4):
	print('\n' * lines)

xx = exit

if __name__ == '__main__':
	df = utils.loadDataExcel()
	space()
	# print(df.head())
	print(df.columns)

	renamer = {'Unnamed: 13' : 'Index',
		'SA2 Code': 'SA2Code',
		'SA2 Name': 'SA2Name'}
	adf = df.rename(columns=renamer)

	space()
	# print(df.head())

	base = {}

	for sa2_name, df in adf.groupby('SA2Name'):
		assert len(df.SA2Code.unique()) == 1
		sa2_code = int(df.SA2Code.iloc[0])

		df = df.sort_values('Year')

		space()
		print(sa2_name, sa2_code)
		print(df.head())

		by_year = [OrderedDict(year = int(tup.Year), index = float(tup.Index)) for tup in df.itertuples()]
		
		base[sa2_code] = OrderedDict()
		base[sa2_code]['postcode'] = 0
		base[sa2_code]['sa2_name'] = sa2_name
		base[sa2_code]['by_year'] = by_year
		# break

	# print(yaml.dump(base, default_flow_style=False))
	output = utils.normabs('./output/data.yml')
	with open(output, 'w') as f:
		yaml.dump(base, f, default_flow_style=False)

