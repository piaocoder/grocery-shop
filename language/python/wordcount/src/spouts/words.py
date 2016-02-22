from __future__ import absolute_import, print_function, unicode_literals

import itertools
from streamparse.spout import Spout


class WordSpout(Spout):

    def initialize(self, stormconf, context):
        self.sentences = [
            "She advised him to take a long holiday, so "
            "he immediately quit work and took a trip around the world",
            "I was very glad to get a present from her",
            "He will be here in half an hour",
            "She saw him eating a sandwich",
        ]
        # self.words = itertools.cycle(['dog', 'cat',
                                      # 'zebra', 'elephant'])
        self.words = itertools.cycle(self.sentences)

    def next_tuple(self):
        word = next(self.words)
        self.emit([word])

    def ack(self, tup_id):
        print('+++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        print('Words ack:+++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        print('+++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        print('Words fail:+++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++++++++++')
        pass
