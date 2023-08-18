from typing import List
import unittest
from llama import LLMEngine
from llama import Type, Context
import os


class Document(Type):
    message: str = Context("a single document or message about a technical system")


class Topics(Type):
    topics: List[str] = Context("a list of one-word system components")
    summary: str = Context("a short summary of the message")


def preprocess_data_into_messages(data):
    data = data.split("\n")
    return [d for d in data if d]


class TestUnblockedPrompt(unittest.TestCase):
    def test_unblocked_custom_prompt(self):
        llm = LLMEngine(id="create_topics")

        data_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data/unblocked/data_from_unblocked_s3.txt",
        )
        with open(data_path, "r") as f:
            data = f.read()
        docs = preprocess_data_into_messages(data)
        document = docs[0]
        document_obj = Document(
            message=document, topic_type="one-word system components"
        )
        value = llm(
            document_obj,
            output_type=Topics,
        )
        print(value)
