
import os.path as osp
import yaml

from flask import Flask, request
app = Flask(__name__, static_url_path='')

from utils import normabs

@app.route('/')
def hello_world():
    msg = [
    	'Hi! You\'ve reached the Analytics Server for Aged Friendly Canberra.'
    	'We are Project77, a GovHack 2018 team making Canberra better for older people :D']

    return ' '.join(msg)
    # return app.send_static_file('./index.html')

@app.route('/data')
def data():
	path = '../output/data.yml'
	path = normabs(path)
	assert osp.isfile(path)

	with open(path, 'r') as f:
		y = yaml.load(f)

	return str(y)