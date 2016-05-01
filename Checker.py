from collections import defaultdict
import Splitter

class Checker():

    def __init__(self):
        self.unknown = 'unknown word'

        self.dictionary = set('\n')
        self.counters = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

        self.window_left = 1
        self.window_right = 1

        self.dict_delay = self.window_left


    def train(self, filenames):
        for each in filenames:
            file = open(each, 'r');
            string = file.read()

            words = Splitter.detect_const(Splitter.imp_split(
                Splitter.delimiters, string, Splitter.detached
            ))

            window = ['\n', '\n', words[0]]

            dict_delayed = []

            for new_word in words[1:]:
                window[0] = window[1]
                window[1] = window[2]
                window[2] = new_word

                print 'Window:  [{}, {}, {}]'.format(repr(window[0]), repr(window[1]), repr(window[2]))

                if window[1] in self.dictionary:
                    index_cur = window[1]
                else:
                    index_cur = self.unknown

                if window[2] in self.dictionary:
                    index_next = window[2]
                else:
                    index_next = self.unknown

                if window[0] in self.dictionary:
                    index_prev = window[0]
                else:
                    index_prev = self.unknown

                print 'Indexes: [{}] [{}] [{}]'.format(repr(index_cur), repr(index_next), repr(index_prev))

                self.counters[index_cur][index_next][index_prev] += 1

                print 'Counter: {}'.format(repr(self.counters[index_cur][index_next][index_prev]))

                for i in range(len(dict_delayed)):
                    dict_delayed[i] = (dict_delayed[i][0], dict_delayed[i][1] - 1)
                    if dict_delayed[i][1] == 0:
                        self.dictionary.add(dict_delayed[i][0])
                        dict_delayed.pop(i)

                dict_delayed.append((window[1], 1))

                print 'Dict:    {}'.format(self.dictionary)
                print 'Delayed: {}'.format(map(lambda x: x[0], dict_delayed))
                print '\n\n'



cc = Checker()
cc.train(['Examples_train/easy_ex.py'])
