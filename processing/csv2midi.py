import sys

import py_midicsv as pm
import os

if __name__ == "__main__":
	midi_dir = sys.argv[1]
	csv_dir = sys.argv[2]

	os.makedirs(midi_dir, exist_ok=True)

	for file in os.listdir(csv_dir):
		path = f'{csv_dir}/{file}'
		if path[-3:] == "txt":
			with open(f"{midi_dir}/{file[:-4]}.mid", "wb") as output_file:
				midi_object = pm.csv_to_midi(path)
				pm.FileWriter(output_file).write(midi_object)
