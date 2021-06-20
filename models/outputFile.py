import json


def save_json(path_output, data):
	with open(path_output, 'w') as fp:
		json.dump(data, fp)
