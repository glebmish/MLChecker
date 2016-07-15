from collections import defaultdict, deque, namedtuple
import Splitter


def inc(x):
    return x + 1

def dec(x):
    return x - 1

def id(x):
    return x

def multidict_operation(mdict, indexes, operation):
    if len(indexes) == 1:
        mdict[indexes[0]] = operation(mdict[indexes[0]])
        return mdict[indexes[0]]
    return multidict_operation(mdict[indexes[0]], indexes[1:], operation)


def multidict_cycle(mdict, dimensions, operation):
    if dimensions == 1:
        for key in mdict:
            mdict[key] = operation(mdict[key])
        return
    for key in mdict:
        multidict_cycle(mdict[key], dimensions - 1, operation)


def print_cell(x, indexes):
    print('counters' + repr(indexes) + ': ' + repr(x))
    return


def multidict_cycle_indexes(mdict, dimensions, operation, indexes=[]):
    if dimensions == 1:
        for key in mdict:
            mdict[key] = operation(mdict[key], indexes + [key])
        return
    for key in mdict:
        multidict_cycle_indexes(mdict[key], dimensions - 1, operation, indexes + [key])


def multidict(dimensions):
    if dimensions == 1:
        return defaultdict(lambda : 0.0)
    return defaultdict(lambda : multidict(dimensions - 1))

class Checker:

    def __init__(self, window_left=1, window_right=1):
        self.unknown = 'unknown word'

        self.window_left = window_left
        self.window_right = window_right
        self.window_len = self.window_left + self.window_right + 1

        self.dict_delay = self.window_left

        self.bound_probability = 0.01

        self.dictionary = set('\n')
        self.counters = multidict(self.window_left + 1 + self.window_right)

    def train(self, filenames):
        for each in filenames:
            file = open(each, 'r');
            string = file.read()

            words = Splitter.imp_split(Splitter.detect_const(string))

            # initialize window
            window = ['\n'] * (self.window_left + 1)
            for word in words[:self.window_right]:
                window.append(word)
            cur_word_index = self.window_left

            # initialize queue for delayed words and declare class for this words
            dict_delayed = deque()
            class Delayed:
                def __init__(self, word, delay):
                    self.word = word
                    self.delay = delay

            # process training for each word
            for new_word in words[self.window_right:]:
                # shift window
                for i in range(0, self.window_len - 1):
                    window[i] = window[i + 1]
                window[self.window_len - 1] = new_word

                # debug print
                print('Window:  ' + repr(window))

                # make indexes (current is first)
                indexes = [window[cur_word_index] if window[cur_word_index] in self.dictionary else self.unknown]
                for word in window:
                    if word is not window[cur_word_index]:
                        indexes.append(word if word in self.dictionary else self.unknown)

                # debug print
                print('Indexes: ' + repr(indexes))

                # increment to cell pointed by list of indexes
                multidict_operation(self.counters, indexes, inc)

                # debug print
                print('Counter: ' + repr(multidict_operation(self.counters, indexes, id)))

                # adding current word to delayed dict if necessary
                if window[cur_word_index] not in self.dictionary:
                    cur_word_delay = self.dict_delay - sum([delayed.delay for delayed in dict_delayed])
                    dict_delayed.append(Delayed(window[cur_word_index], cur_word_delay))

                # move first object to dictionary if delay is expired
                if len(dict_delayed) and dict_delayed[0].delay == 0:
                    self.dictionary.add(dict_delayed[0].word)
                    dict_delayed.popleft()
                if len(dict_delayed):
                    dict_delayed[0].delay -= 1

                # debug print
                print('Dict:    ' + repr(self.dictionary))
                print('Delayed: ' + repr([delayed.word for delayed in dict_delayed]))
                print('\n')

        # decrement each cell in counters[self.unknown]
        multidict_cycle(self.counters[self.unknown], self.window_len - 1, dec)

        # debug print
        multidict_cycle_indexes(self.counters, self.window_len, print_cell)

#TODO: refactor check
    def check(self, filenames):
        print '\n\n'

        for each in filenames:
            file = open(each, 'r')

            string = file.read()

            words = Splitter.detect_const(Splitter.imp_split(
                Splitter.delimiters, string, Splitter.detached
            ))

            window = ['\n', '\n', words[0]]

            for new_word in words[1:]:
                window[0] = window[1]
                window[1] = window[2]
                window[2] = new_word

                print 'Window:  [{}, {}, {}]'.format(repr(window[0]), repr(window[1]), repr(window[2]))

                if window[1] in self.dictionary:
                    index_cur = window[1]
                else:
                    index_cur = self.unknown

                if window[0] in self.dictionary:
                    index_prev = window[0]
                else:
                    index_prev = self.unknown

                if window[2] in self.dictionary:
                    index_next = window[2]
                else:
                    index_next = self.unknown

                print 'Indexes: [{}] [{}] [{}]'.format(repr(index_cur), repr(index_prev), repr(index_next))

                # this part is undiscussed and likely to be wrong
                if index_cur == self.unknown:
                    if self.counters[index_cur][index_prev][index_next] == 0:
                        print 'Word {} can be wrong'.format(window[1])
                else:
                    if self.counters[index_cur][index_prev][index_next] <\
                            self.counters[self.unknown][index_prev][index_next]:
                        print 'Word {} can be wrong'.format(window[1])
                #

                print


cc = Checker()
cc.train(['Examples_train/easy_ex.py'])
#cc.check(['Examples_check/easy_ch.py'])
