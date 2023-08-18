from llama import Type, Context, LLMEngine

import unittest

from multi_model_test import run_models
from multi_model_test import MultiModelTest


class TestSaveData(MultiModelTest):
    def setUp(self) -> None:
        return super().setUp()

    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_save_data(self):
        class Question(Type):
            question: str = Context("question")

        class Answer(Type):
            answer: str = Context("answer")

        class Score(Type):
            score: float = Context("score")

        self.llm.clear_data()
        x = self.llm.save_data(Question(question="What is 3+4?"))
        print(x)
        assert x == {"dataset": "e8499b356fa0d150e1af6b399de73c6a"}
        x = self.llm.save_data(Answer(answer="The answer is 8."))
        print(x)

        x = self.llm.save_data(Score(score=3.2))
        print(x)
        x = self.llm.save_data([Score(score=4.3), Score(score=1.4), Score(score=5.3)])
        print(x)

        # This handles an llm going from Question->Answer AND Answer->Question
        # Because the which type is "input" and "output" don't really matter here
        x = self.llm.save_data(
            [Question(question="What is 2+1?"), Answer(answer="The answer is 3.")]
        )
        print(x)

        response = self.llm.clear_data()
        print(response)
        assert response == {"deleted": 5}

    def test_save_data_multiple(self):
        class Question(Type):
            question: str = Context("question")

        llm = LLMEngine(id="test_save_data_1")
        llm2 = LLMEngine(id="test_save_data_2")

        self.llm.clear_data()
        x = llm.save_data(Question(question="What is 3+4?"))
        print(x)
        assert x == {"dataset": "e8499b356fa0d150e1af6b399de73c6a"}
        x = llm2.save_data(Question(question="What is 3+4?"))
        print(x)
        assert x == {"dataset": "e8499b356fa0d150e1af6b399de73c6a"}

        response = llm.clear_data()
        assert response == {"deleted": 1}

        response = llm2.clear_data()
        assert response == {"deleted": 1}
