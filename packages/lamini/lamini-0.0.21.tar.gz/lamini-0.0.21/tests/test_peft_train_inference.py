import unittest
from llama import QuestionAnswerModel


class TestPeftTrainInference(unittest.TestCase):
    def test_peft_inference(self):
        data = [
            {"question": "What kind of exercise is good for me?", "answer": "Running"},
            {"question": "hello", "answer": "hello"},
            {"question": "What is the best way to get fit?", "answer": "Running"},
            {"question": "tell me something", "answer": "eat and stay healthy"},
            {"question": "Hey", "answer": "Hey"},
            {"question": "Whats your name?", "answer": "My name is Llama"},
            {"question": "What is the best way to get fit?", "answer": "Running"},
            {"question": "What kind of exercise is good for me?", "answer": "Running"},
            {"question": "What is the best way to get fit?", "answer": "Running"},
            {"question": "What kind of exercise is good for me?", "answer": "Running"}
        ]
        model = QuestionAnswerModel("hf-internal-testing/tiny-random-gpt2")
        model.load_question_answer(data)
        model.train(enable_peft=True)
        print("new model: " + model.model_name)
        new_model = QuestionAnswerModel(model.model_name)
        answer = new_model.get_answer("What kind of exercise is good for me?")
        print(answer)