from llama import BasicModelRunner
import unittest


class TestBasicModelRunner(unittest.TestCase):
    def test_basic_model_runner(self):
        print("Testing BasicModelRunner...")
        model = BasicModelRunner("hf-internal-testing/tiny-random-gpt2")

        # 10 examples
        model.load_data(
            [
                {"input": "What kind of exercise is good for me?", "output": "Running"},
                {
                    "input": "What kind of exercise is super for me?",
                    "output": "Running",
                },
                {
                    "input": "What kind of exercise is awesome for me?",
                    "output": "Running",
                },
                {"input": "What kind of exercise is cute for me?", "output": "Running"},
                {
                    "input": "What kind of exercise is poggers for me?",
                    "output": "Running",
                },
                {
                    "input": "What kind of exercise is bad for me?",
                    "output": "Not running",
                },
                {
                    "input": "What kind of exercise is terrible for me?",
                    "output": "Not running",
                },
                {
                    "input": "What kind of exercise is horrible for me?",
                    "output": "Not running",
                },
                {
                    "input": "What kind of exercise is sad for me?",
                    "output": "Not running",
                },
                {
                    "input": "What kind of exercise is meh for me?",
                    "output": "Not running",
                },
            ],
            verbose=True,
        )

        model.train(is_public=True)
        print("new model: " + model.model_name)

        # Test 2 types of evaluation
        model.evaluate()
        print(model.evaluation)

        results = model.evaluate()
        print(results)

        # Test single inference
        output = model("What kind of exercise is OK for me?")
        print(output)

        # Test batch inference
        outputs = model(
            [
                "What kind of exercise is OK for me?",
                "What kind of exercise is so-so for me?",
            ]
        )
        print(outputs)
