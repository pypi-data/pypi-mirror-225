import unittest

from llama.runners.llama_v2_runner import LlamaV2Runner


class TestLlamaModelRunner(unittest.TestCase):
    def test_llama_model_runner(self):
        print("Testing LlamaModelRunner...")

        DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""
        model = LlamaV2Runner(
            "hf-internal-testing/tiny-random-gpt2", DEFAULT_SYSTEM_PROMPT
        )
        model.clear_data()
        # 10 examples
        model.load_data(
            [
                {
                    "user": "What kind of exercise is good for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is super for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is awesome for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is cute for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is poggers for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is bad for me?",
                    "system": DEFAULT_SYSTEM_PROMPT,
                    "output": "Not running",
                },
                {
                    "user": "What kind of exercise is terrible for me?",
                    "output": "Not running",
                },
                {
                    "user": "What kind of exercise is horrible for me?",
                    "output": "Not running",
                },
                {
                    "user": "What kind of exercise is sad for me?",
                    "output": "Not running",
                },
                {
                    "user": "What kind of exercise is meh for me?",
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
