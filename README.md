# Research Paper Recommender

This project is aimed at helping researchers and people who read scientific papers find new papers that might be of interest to them. It leverages [arXiv](https://arxiv.org/) and recent developments in *word embeddings* (using a popular library [gensim](https://radimrehurek.com/gensim/)) to automatically fetch new papers for a given category and then add them to a specified folder if they are found to be similar to a list of given papers already in the user's library.

## State of the project

Currently the project is made up of three python scripts : a) `reader.py`  b) `doc2vec.py`  c) `feed.py`.

##### reader.py

Scans an input directory (specified in *init.sh* as `INPUT_FILE_PATH`) and extracts the first few lines of every pdf file. The extracted text is saved in a csv format at *library.corr* along with the filename of the pdf file.

#### doc2vec.py

This script takes as input the previously generated *library.corr* and generates a Doc2Vec model which transforms the list of research articles into vectors.

#### feed.py

We then leverage the API created by arXiv to fetch new papers of a given category and based on the average similarity score (based on *cosine similarity*) and a specified threshold the papers are added to an output folder and a notification (based on linux ubuntu *notify-send*) is issued to the user.

## Future

The options for extending this project are many. From including other methods of turning documents into vectors (*bag of words*, *tf-idf*) to more elaborate ways of reading in pdf files and extracting text.

## Getting Started

You first need to specify some environment variables in *init.sh*. Then use `source init.sh` to include the variables into the running shell. The sequence of running the python scripts is reader -> doc2vec -> feed. Currently, reader.py needs *python 3* to run (an issue soon to be resolved). You can then use doc2vec to generate the model. Then you have the option of instantly running `feed.py` (would need to edit some code) or run it as a background process using `nohup python feed.py &`.

### Prerequisities

You need to have the following installed :

* Python 2.7.x or newer
* Pip
