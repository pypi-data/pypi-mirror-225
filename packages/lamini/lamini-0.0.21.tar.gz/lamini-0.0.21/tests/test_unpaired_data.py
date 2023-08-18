import unittest
from llama import LLMEngine
from llama import Type, Context


# Input
class Question(Type):
    question: str = Context("A question")


# Context
class Document(Type):
    document: str = Context("A single document")


# Output
class Answer(Type):
    answer: str = Context("An answer to the question")


class TestCreateDocs(unittest.TestCase):
    def test_create_with_add_data(self):
        llm = LLMEngine(id="create_answer")
        llm.clear_data()
        question = Question(question="What is Lamini?")
        answer = llm(input=question, output_type=Answer)
        print(answer)
        llm.add_data(
            [
                Document(document="Lamini is the world’s most powerful LLM engine."),
            ]
        )
        print("\n\nWITH DOCS AS TYPES\n\n")
        answer = llm(input=question, output_type=Answer)
        print(answer)
        llm.clear_data()
        llm.add_data(
            [
                [Document(document="Lamini is the world’s most powerful LLM engine.")],
            ]
        )
        print("\n\nWITH DOCS AS LISTS\n\n")
        answer = llm(input=question, output_type=Answer)
        print(answer)
