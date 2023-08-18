from llama.runners.llama_v2_runner import LlamaV2Runner
import unittest

class TestLlamaV2Runner(unittest.TestCase):
    def test_llama_v2_runner(self):
        print("Testing LlamaV2Runner...")
        model = LlamaV2Runner(model_name="hf-internal-testing/tiny-random-gpt2")

        # different ways of loading data
        # 10 examples
        # method 1: list of dicts
        model.load_data(
            [
                {
                    "user": "What kind of exercise is good for me?", 
                    "output": "Running"
                },
                {
                    "user": "What kind of exercise is super for me?",
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is awesome for me?",
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is cute for me?", 
                    "output": "Running"
                },
                {
                    "user": "What kind of exercise is poggers for me?",
                    "output": "Running",
                },
                {
                    "user": "What kind of exercise is bad for me?",
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
        
        # method 2: csv file (can also be a dataframe)
        # model.load_data_from_csv("filename.csv", verbose=True)

        # train the model
        model.train(is_public=True, finetune_args={'learning_rate': 1e-5})
        print("new model: " + model.model_name)

        # evaluate the model
        # Test 2 types of evaluation
        print("\neval method 1 (model.evaluate())...")
        results = model.evaluate()
        print(results)
        
        print("\neval method 2 (model.get_eval_results())...")
        results = model.get_eval_results()
        print(results)

        # run inference on the model
        # Test single inference
        print("\nTest single inference...")
        output = model("What kind of exercise is OK for me?", system_prompt="answer like you are ifit bot. answer in 2-3 lines only and be honest.")
        print(output)

        # Test batch inference
        print("\nTest batch inference...")
        outputs = model(
            [
                "What kind of exercise is OK for me?",
                "What kind of exercise is so-so for me?",
            ],
            system_prompt="answer like you are ifit bot. answer in 2-3 lines only and be honest."
        )
        print(outputs)
