import re

from streamparse.bolt import Bolt


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
