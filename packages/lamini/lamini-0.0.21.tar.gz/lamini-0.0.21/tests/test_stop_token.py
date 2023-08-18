from llama import Type, Context, LLMEngine

import unittest


class TestStopToken(unittest.TestCase):
    def test_stop_token(self):
        class Question(Type):
            question: str = Context("question")

        class Answer(Type):
            answer: str = Context("answer")

        llm = LLMEngine(
            id="stop_token", model_name="hf-internal-testing/tiny-random-gpt2"
        )

        def answer_question(question: Question, stop_token=[]) -> Answer:
            story = llm(input=question, output_type=Answer, stop_token=stop_token)

            return story

        question = Question(
            question="What is a llama?",
        )

        answer = answer_question(question=question)

        print(f"Answer without stop token: {answer.answer}")

        stop_token = answer.answer.split()[0]
        answer_with_stop_token = answer_question(
            question=question, stop_token=stop_token
        )

        print(f"Answer with stop token: {answer_with_stop_token.answer}")

        assert len(answer_with_stop_token.answer) < len(
            answer.answer
        ), "Stop token test failed"
