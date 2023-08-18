from llama import Type, Context, LLMEngine

import unittest

from multi_model_test import run_models
from multi_model_test import MultiModelTest


class TestAddData(MultiModelTest):
    def setUp(self) -> None:
        return super().setUp()

    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_add_data(self):
        class Question(Type):
            question: str = Context("question")

        class Answer(Type):
            answer: str = Context("answer")

        class Score(Type):
            score: float = Context("score")

        self.llm.clear_data()
        self.llm.add_data(Question(question="What is 3+4?"))
        self.llm.add_data(Answer(answer="The answer is 8."))
        self.llm.add_data(Score(score=3.2))
        self.llm.add_data([Score(score=4.3), Score(score=1.4), Score(score=5.3)])

        # This handles an llm going from Question->Answer AND Answer->Question
        # Because the which type is "input" and "output" don't really matter here
        self.llm.add_data(
            [Question(question="What is 2+1?"), Answer(answer="The answer is 3.")]
        )

        question = Question(question="Why is 2+2?")
        print(f"Input is {question}")
        generated_answer = self.llm(question, output_type=Answer)
        print(generated_answer)

        answer = Answer(answer="The answer is 4.")
        print(f"Input is {answer}")
        generated_question = self.llm(answer, output_type=Question)
        print(generated_question)

        # You can provide more pairs

        examples = [
            [Question(question="What is 2+5?"), Answer(answer="The answer is 7.")],
            [Question(question="What is 6+2?"), Answer(answer="The answer is 8.")],
        ]
        self.llm.add_data(examples)

        # # You can provide data with different types, paired or unpaired, together

        examples = [
            [Question(question="What is 7+3?"), Answer(answer="The answer is 10.")],
            [Score(score=2.5), Score(score=3.0)],
        ]
        self.llm.add_data(examples)

        answer = Answer(answer="The answer is 14.")
        print(f"Input is {answer}")
        generated_question = self.llm(answer, output_type=Question)
        print(generated_question)
