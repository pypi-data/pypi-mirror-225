from typing import List

from llama import Type, Context

import unittest


class TestQuestion2(unittest.TestCase):
    def testQuestion2(self):
        class QAPair(Type):
            question: str = Context("question")
            answer: str = Context("answer")

        class QandAPairs(Type):
            q_a_pairs: List[QAPair] = Context("describe me")

        q_a = QAPair(
            question="What is this?", answer="This is you.", test_field_wwoooo="ff"
        )
        x = QandAPairs(q_a_pairs=[q_a])
        print(x.schema())
