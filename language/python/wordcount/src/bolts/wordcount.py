from __future__ import absolute_import, print_function, unicode_literals

import re
from collections import Counter
from streamparse.bolt import Bolt


class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]
        self.counts[word] += 1
        self.emit([word, self.counts[word]])


class WordSaver(Bolt):
    def initialize(self, conf, ctx):
        self.name = "bamboo"

    def process(self, tup):
        word = tup.values[0]
        wordCounter = tup.values[1]
        self.log('(%s)%s: %d' % (self.name, word, wordCounter))


class SentenceSplitterBolt(Bolt):

    def process(self, tup):
        sentence = tup.values[0]  # extract the sentence
        # get rid of punctuation
        sentence = re.sub(r"[,.;!\?]", "", sentence)
        words = [[word.strip()]
                 for word in sentence.split(" ") if word.strip()]
        if not words:
            # no words to process in the sentence, fail the tuple
            self.fail(tup)
            return

        self.emit_many(words)
        # tuple acknowledgement is handled automatically
