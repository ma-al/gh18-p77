
import os.path as osp
import pandas as pd
import numpy as np

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

def translatePopulation():
	df = utils.loadExcel('raw/Population Projections.xlsx')
	# space()
	# print(df.head())
	# print(df.columns)

	renamer = {'Unnamed: 13' : 'Index',
		'SA2 Code': 'SA2Code',
		'SA2 Name': 'SA2Name',
		'Total>=65': 'ElderPopulation',
		'TOTAL': 'TotalPopulation'}
	adf = df.rename(columns=renamer)

	space()
	# print(df.head())

	base = {}

	for sa2_name, df in adf.groupby('SA2Name'):
		assert len(df.SA2Code.unique()) == 1
		sa2_code = int(df.SA2Code.iloc[0])

		df = df.sort_values('Year')

		# space()
		# print(sa2_name, sa2_code)
		# print(df.head())

		by_year = []
		for tup in df.itertuples():

			year = OrderedDict()
			year['year'] = int(tup.Year)
			year['index'] = float(tup.Index)
			year['elder_population'] = int(tup.ElderPopulation)
			year['total_population'] = int(tup.TotalPopulation)

			by_year.append(year)
		
		base[sa2_code] = OrderedDict()
		base[sa2_code]['postcode'] = 0
		base[sa2_code]['sa2_name'] = sa2_name
		base[sa2_code]['by_year'] = by_year
		# break

	# print(yaml.dump(base, default_flow_style=False))
	# xx()

	output = utils.normabs('./output/data.yml')
	with open(output, 'w') as f:
		yaml.dump(base, f, default_flow_style=False)

	return base

def crunchAgedCare():
	path = utils.normabs('raw/Aged Care Services list ACT.xlsx')
	assert osp.isfile(path), path
	adf = pd.read_excel(path, header=1)

	# space()
	# print(adf.columns)
	# space()
	# print(adf.head())
	# xx()

	space()
	suburbs = []
	for suburb, df in adf.groupby('Physical Address Suburb'):

		# print(suburb)
		# print(df.head())
		# print()
		# xx()

		d = OrderedDict()
		d['sa2_name'] = suburb.title()
		d['postcode'] = int(df['Physical Address Post Code'].iloc[0])
		d['aged_care_svc_count'] = len(df)

		suburbs.append(d)
		# break

	# print(suburbs)
	# print(yaml.dump(suburbs, default_flow_style=False))
	# xx()

	output = utils.normabs('./output/aged_services_counts.yml')
	with open(output, 'w') as f:
		yaml.dump(suburbs, f, default_flow_style=False)

	df = pd.DataFrame(suburbs)
	df.to_csv('./output/aged_services_counts.csv', index=False)
	# print(df)

def crunchEverything():
	path = utils.normabs('raw/Aged care places ACT.xlsx')
	assert osp.isfile(path), path
	adf = pd.read_excel(path, header=0)

	renamer = {
		'Total Sum of Residential Places': 'ResidentialPlaces',
		'Total Sum of Home Care Low Places': 'LowPlaces',
		'Total Sum of Home Care High Places': 'HighPlaces',
		'Total Sum of Transition Care Places': 'TransitionPlaces',
		'Unnamed: 4': 'TotalPlaces'}
	adf = adf.rename(columns=renamer)

	# space()
	# print(adf.columns)
	# print(adf.head())

	path = utils.normabs('raw/Bus stops by suburbs.xlsx')
	assert osp.isfile(path), path
	bdf = pd.read_excel(path)
	bdf = bdf.set_index('Suburb')
	bdf = bdf.rename(columns=dict(Count='BusStops'))

	# space()
	# print(bdf.columns)
	# print(bdf.head())
	
	path = utils.normabs('raw/Public furniture by suburb.xlsx')
	assert osp.isfile(path), path
	fdf = pd.read_excel(path)
	fdf = fdf.set_index('Suburb')
	fdf = fdf.rename(columns=dict(Count='Furniture'))

	# space()
	# print(fdf.columns)
	# print(fdf.head())

	df = pd.concat([bdf, fdf, adf], axis='columns')
	df = df.reset_index()
	df = df.rename(columns=dict(index='SuburbName'))

	df.SuburbName = df.SuburbName.apply(str.title)
	df = df.fillna(0)
	cols = 'BusStops Furniture ResidentialPlaces LowPlaces HighPlaces TransitionPlaces TotalPlaces'.split()
	df[cols] = df[cols].astype(int)

	# df = df.set_index('SuburbName')
	# space()
	# print(df.columns)
	# print(df.head())

	df.to_csv('./output/merged.csv', index=False)
	return df
	

if __name__ == '__main__':
	pdf = translatePopulation()
	# aged_data = crunchAgedCare()
	mdf = crunchEverything()

	print(len(pdf))
	print(len(mdf))


	

