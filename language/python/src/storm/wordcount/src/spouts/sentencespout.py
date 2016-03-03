#!/usr/bin/env python
#coding:utf8
import itertools
from streamparse.spout import Spout


class SentenceSpout(Spout):

    def initialize(self, stormconf, context):
        """initialize；初始化函数，在spout进入主循环之前调用

        :param stormconf:
        :param context:
        """
        self.sentences = [
            "She advised him to take a long holiday, so "
            "he immediately quit work and took a trip around the world",
            "I was very glad to get a present from her",
            "He will be here in half an hour",
            "She saw him eating a sandwich",
        ]
        self.sentences = itertools.cycle(self.sentences)

    def next_tuple(self):
        """next_tuple:不断循环调用"""
        sentence = next(self.sentences)
        self.emit([sentence])

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
