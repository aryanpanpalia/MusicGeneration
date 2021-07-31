import os
from processing import carycompressed2csv, csv2midi

if __name__ == '__main__':
    reconstruct = True

    os.system(f"python ../processing/midi2csv.py ./archive ./csvs")
    os.system(f"python ../processing/csv2carycompressed.py ./csvs ./carycompressed")
    os.system(f"python ../processing/carycompressed2data.py ./carycompressed ./train.txt ./test.txt ./valid.txt")

    if reconstruct:
        carycompressed2csv.process(
            './test.txt',
            './reconstructed_csv.txt',
            './reconstructed_img.png'
        )
        # Im using a hack-y method so it should throw an error and will result in an extra, empty .mid file
        try:
            os.system('python ../processing/csv2midi.py ./ ./')
        except ValueError:
            pass
