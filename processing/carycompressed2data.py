import os
import sys

if __name__ == '__main__':
	carycompressed_path = sys.argv[1]
	train_path = sys.argv[2]
	test_path = sys.argv[3]
	valid_path = sys.argv[4]

	open(train_path, 'w').close()
	train = open(train_path, 'a')

	open(test_path, 'w').close()
	test = open(test_path, 'a')

	open(valid_path, 'w').close()
	valid = open(valid_path, 'a')

	for file in os.listdir(carycompressed_path):
		if file[-5] == "0":
			test.write(open(f'{carycompressed_path}/{file}').read())
			valid.write(open(f'{carycompressed_path}/{file}').read())
		else:
			train.write(open(f'{carycompressed_path}/{file}').read())
