# coding=utf-8
from collections import defaultdict
from math import log
import codecs


def divide(dataset, pc_left_bound, pc_right_bound):
    """Divides one dataset on two
    :param dataset: dataset to divide
    :param pc_left_bound: percent from which all records will be stored in the inner ds
    :param pc_right_bound: percent to which all records will be stored in the inner ds
    :return: two datasets: outer and inner
    """
    ds_outer = DataSet()
    ds_inner = DataSet()
    ct_left_bound = int(dataset.len / 100.0 * pc_left_bound)
    ct_right_bound = int(dataset.len / 100.0 * pc_right_bound)

    for i in range(dataset.len):
        if i in range(ct_left_bound, ct_right_bound):
            ds_inner.add(dataset.dataset[i])
        else:
            ds_outer.add(dataset.dataset[i])
    return ds_outer, ds_inner


class DataSet:
    def __init__(self, filename = ''):
        self.dataset = []
        self.pos = 0
        self.len = 0
        if filename == '':
            return

        with codecs.open(filename, 'r', 'utf-8') as file:
            for line in file:
                self.dataset.append(tuple(line.split()))
                self.len += 1

    def __iter__(self):
        return self

    def next(self):
        self.pos += 1
        if self.pos == len(self.dataset):
            raise StopIteration
        else:
            return self.dataset[self.pos - 1]

    def add(self, record):
        """Adds record in dataset"""
        self.dataset.append(record)
        self.len += 1


class Classifier:
    def __init__(self):
        raise Exception("Abstract")

    def train(self, dataset):
        raise Exception("Abstract")

    def check(self, dataset):
        raise Exception("Abstract")

    def classify(self, value):
        raise Exception("Abstract")


class BayesClassifier(Classifier):
    def __init__(self, functor):
        self.features = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.000001)))
        self.get_features = functor
        self.count = defaultdict(lambda: 0.0)

    def train(self, dataset):
        """Collects statistics from training dataset"""
        for value, type in dataset:
            val_features = self.get_features(value)
            for featName in val_features:
                self.features[type][featName][val_features[featName]] += 1
            self.count[type] += 1

        for type in self.features:
            for featName in self.features[type]:
                sum_feat = sum(self.features[type][featName].values())
                for letter in self.features[type][featName]:
                    self.features[type][featName][letter] /= sum_feat
        sum_ct = sum(self.count.values())
        for type in self.count:
            self.count[type] /= sum_ct

    def check(self, dataset):
        """Checks the false percent in testing dataset. Returns false percent and false records"""
        pos_neg_table = dict( (t, dict([(t, 0) for t in self.features])) for t in self.features)
        for value, type in dataset:
            cl_type = self.classify(value)
            pos_neg_table[type][cl_type] += 1
        recalls = {}
        precisions = {}
        for type in self.features:
            recalls[type] = float(pos_neg_table[type][type]) / (sum(pos_neg_table[type].values()) + 0.001)
            precisions[type] = float(pos_neg_table[type][type]) / \
                               (sum(pos_neg_table[cl_type][type] for cl_type in pos_neg_table) + 0.001)
        recall = sum(recalls.values()) / len(recalls)
        precision = sum(precisions.values()) / len(precisions)
        return recall, precision

    def classify(self, value):
        """Classifies value based on collected statistics"""
        value = value.lower()
        val_features = self.get_features(value)

        max_type = None
        max_prob = -1000

        for type in self.features:
            prob = log(self.count[type])

            for featName in self.features[type]:
                prob += log(self.features[type][featName][val_features[featName]])
            if max_prob < prob:
                max_prob = prob
                max_type = type

        return max_type
