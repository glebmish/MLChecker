import Splitter

with open('./Examples_train/Bayes_Classifier.py', 'r') as file:
    string = file.read()
    words = Splitter.detect_const(Splitter.imp_split(Splitter.delimiters, string, Splitter.detached))
    print words
