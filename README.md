# MusicGeneration
This project attempts to generate classical music using a word-based LSTM.
## Data
I stored the midi files I used into `./data/archive.`Songs are grouped by composer, however, when I process the files I do so recursively.

To process the midi files into data to feed into the machine learning model, I used a slightly modified version of https://github.com/aryanpanpalia/caryCompressionMIDICSV. 

## Model
I used the word-based text generation model from https://github.com/pytorch/examples/tree/master/word_language_model. 

## Experiments
I tracked my experiments in `experiments.txt`.

## Results
The results can be seen in `./results`.