from llama import Type, Context, LLMEngine

import unittest


class TestOutputList(unittest.TestCase):
    def test_output_list(self):
        class Topics(Type):
            topics: list = Context("system components")

        class Message(Type):
            message: str = Context("the message")

        llm = LLMEngine(id="output_list")

        def get_topics(message: Message) -> Topics:
            topics = llm(input=message, output_type=Topics)

            return topics

        message = Message(
            message="llamas and other animals",
        )

        topics = get_topics(message=message)

        print(topics)
