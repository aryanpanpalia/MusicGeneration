import sys

import py_midicsv as pm
import os

midi_dir = sys.argv[1]
csv_dir = sys.argv[2]
os.makedirs(csv_dir, exist_ok=True)

for root, dirs, files in os.walk(midi_dir, topdown=False):
	for file in files:
		path = os.path.join(root, file)
		print(path)

		open(f'{csv_dir}/{file[:-4]}.csv', 'w').close()
		try:
			with open(f'{csv_dir}/{file[:-4]}.csv', 'a') as f:
				lines = pm.midi_to_csv(path)
				for line in lines:
					f.write(line)
		except:
			pass
