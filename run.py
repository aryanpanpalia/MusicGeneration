import os
import numpy as np

if __name__ == '__main__':
	ATTEMPT = "5"
	os.makedirs(f"generated{ATTEMPT}", exist_ok=True)
	MIN_TEMP = 0.80
	MAX_TEMP = 1.20
	STEP = 0.01
	for temp in np.arange(MIN_TEMP, MAX_TEMP, STEP):
		temp = np.round(temp, 2)
		print(f"Attempt: {ATTEMPT}; Temperature: {temp}")
		os.system(f"python generate.py --checkpoint experiment{ATTEMPT}.pt --outf generated{ATTEMPT}/generated-{temp}.txt --words 3000 --cuda --temperature {temp}")

	os.system(f"python ./processing/carycompressed2csv.py generated{ATTEMPT} output{ATTEMPT}")
	os.system(f"python ./processing/csv2midi.py ./output{ATTEMPT} ./output{ATTEMPT}")
