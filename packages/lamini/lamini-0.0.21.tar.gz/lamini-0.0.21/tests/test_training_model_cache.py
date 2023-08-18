import random
import time
import unittest

from llama import BasicModelRunner


class TestTrainingModelCache(unittest.TestCase):
    def test_training_model_cache(self):
        data = [
            {"input": "What kind of cat is the best cat?", "output": "meow"},
            {"input": "bark", "output": "woof"},
            {"input": "What is the best cat toy?", "output": "Kitty wand!"},
            {"input": "tell me something", "output": "kittens and puppies"},
            {"input": "hissss", "output": "no"},
            {"input": "Whats your name?", "output": "My name is Ginkgo"},
            {"input": "What is your favorite food?", "output": "Tuna and egg"},
            {
                "input": "What kind of exercise is good for me?",
                "output": "Chasing lizards",
            },
            {"input": "What's your favorite dish to make", "output": "Biscuits"},
            {"input": "who is your best friend", "output": "llama"},
            {"input": str(random.random()), "output": str(random.random())},
        ]

        # Train first model
        start_time = time.time()
        model = BasicModelRunner("hf-internal-testing/tiny-random-gpt2")
        model.load_data(data)
        model.train(is_public=True)
        print("New public model: " + model.model_name)

        model_elapsed_time = time.time() - start_time
        print("\tTime elapsed: " + str(model_elapsed_time) + " seconds")

        # Train another model with the same parameters
        start_time = time.time()
        dupe_model = BasicModelRunner("hf-internal-testing/tiny-random-gpt2")
        dupe_model.load_data(data)
        dupe_model.train(is_public=True)
        print("\nRe-train model with same parameters: " + dupe_model.model_name)

        dupe_model_elapsed_time = time.time() - start_time
        print("\tTime elapsed: " + str(dupe_model_elapsed_time) + " seconds")

        assert model.model_name == dupe_model.model_name
        assert dupe_model_elapsed_time < model_elapsed_time
