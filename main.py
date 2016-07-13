import Splitter

with open('./Examples/Bayes_Classifier.py', 'r') as file:
    string = file.read()
    words = Splitter.imp_split(Splitter.detect_const(string))
    print(words)
