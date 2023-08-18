import unittest

from llama.program.util.run_ai import query_run_embedding
from sklearn.metrics.pairwise import cosine_similarity


class TestEmbedding(unittest.TestCase):
    def test_embedding(self):
        first_prompt = "here is a sentence about llamas"

        first_embedding = query_run_embedding(first_prompt)

        second_prompt = "here is another sentence about llamas"

        second_embedding = query_run_embedding(second_prompt)

        similarity = cosine_similarity(first_embedding, second_embedding)

        print(similarity)
