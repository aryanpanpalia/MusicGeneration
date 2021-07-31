import concurrent.futures
import os
import sys

import numpy as np
from PIL import Image
from tqdm import tqdm


def process(input_file, output_file, output_image):
	pitchCount = 116
	multi = 40

	raw_data = open(input_file).readlines()

	data = []
	for line in raw_data:
		no_rests = line.replace("[REST]", "")
		no_eos = no_rests.replace("<eos>", "\n")
		data.append(no_eos)

	length = 0
	for line in data:
		for char in line:
			if char == " ":
				length += 1
	length += 1

	notes = np.zeros((length, pitchCount), dtype=bool)
	pointerAt = 0
	for line in data:
		for char in line:
			pitch = ord(char) - 33
			if char == " ":
				pointerAt += 1
			else:
				try:
					notes[pointerAt][pitch] = True
				except IndexError:
					print(f"Index error on {input_file}...")
					break

	pointerAt += 1

	outputImage = np.zeros((1080, length * 2 + 2)).astype('uint8')
	shift = 0
	for i in range(length):
		for j in range(87):
			if notes[i + shift][j]:
				outputImage[(86 - j) * 10: (86 - j) * 10 + 10, i * 2: i * 2 + 2] = 255

	open(output_file, 'w').close()
	output = open(output_file, 'a')
	output.write(f"0, 0, Header, 1, 3, {384 // 2}\n")
	output.write("1, 0, Start_track\n")
	output.write("1, 0, Time_signature, 4, 2, 24, 8\n")
	output.write("1, 0, Tempo, 500000\n")
	output.write(f"1, {pointerAt * multi}, End_track\n")
	output.write("2, 0, Start_track\n")
	output.write("2, 0, Text_t, \"random instrument: random person i dunno whatev\"\n")
	output.write("2, 0, Title_t, \"Track 1\"\n")

	for i in range(pointerAt):
		for j in range(87):
			try:
				if notes[i][j] and (i == 0 or not notes[i - 1][j]):
					output.write(f"2, {i * multi}, Note_on_c, 1, {j + 21}, 127\n")
				if not notes[i][j] and i >= 1 and notes[i - 1][j]:
					output.write(f"2, {i * multi}, Note_off_c, 1, {j + 21}, 0\n")
			except IndexError:
				print(f"Index error on {input_file}...")
				break

	output.write(f"2, {pointerAt * multi}, End_track\n")
	output.write("3, 0, Start_track\n")
	output.write("3, 0, Title_t, \"MIDI\"\n")
	output.write("3, 1536, End_track\n")
	output.write("0, 0, End_of_file\n")
	output.flush()
	output.close()

	image = Image.fromarray(outputImage)
	image.save(output_image)


if __name__ == '__main__':
	INPUT_DIR = sys.argv[1]
	OUTPUT_DIR = sys.argv[2]

	os.makedirs(OUTPUT_DIR, exist_ok=True)

	compressedFileNames = os.listdir(INPUT_DIR)
	reconTextFileNames = list(map(lambda filename: f"{OUTPUT_DIR}/reconstructed_{filename}", compressedFileNames))
	reconImageFileNames = list(map(lambda filename: f"{filename[:-4]}.png", reconTextFileNames))
	compressedFileNames = [f"{INPUT_DIR}/{filename}" for filename in compressedFileNames]

	with concurrent.futures.ProcessPoolExecutor() as executor:
		list(
			tqdm(
				executor.map(process, compressedFileNames, reconTextFileNames, reconImageFileNames),
				total=len(compressedFileNames),
				file=sys.stdout,
				desc="Files Processed"
			)
		)
