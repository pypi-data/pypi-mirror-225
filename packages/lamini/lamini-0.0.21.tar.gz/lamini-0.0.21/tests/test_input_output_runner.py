from llama import InputOutputRunner, Type, Context
import unittest
import pandas as pd

class TestInputOutputRunner(unittest.TestCase):
    def test_input_output_runner(self):
        print("Testing InputOutputRunner...")

        class Input(Type):
            instruction: str = Context("instruction")
            is_question: int = Context("whether instruction is a question (1) or not (0))")

        class Output(Type):
            response: str = Context("response to instruction")
            is_positive: int = Context("whether response was positive (1) or not (0)")

        model = InputOutputRunner(
            input_type=Input,
            output_type=Output,
            model_name="hf-internal-testing/tiny-random-gpt2",
        )

        model.load_data(
            [[
                Input(instruction="What kind of exercise is good for me?", is_question=1),
                Output(response="Running", is_positive=1),
            ]],
            verbose=True,
        )

        model.load_data_from_paired_dicts(
            [
                {
                    "input": 
                        {
                            "instruction": "What kind of exercise is good for me?",
                            "is_question": 1,
                        }, 
                    "output": {
                        "response": "Running",
                        "is_positive": 1,
                    },
                },
            ],
            verbose=True,
        )

        # Other methods of loading data
        # Load data from a list of paired dictionaries
        model.load_data_from_paired_lists(
            # Expect data to be formatted as [[input_dict, output_dict], [input_dict, output_dict], ...]
            [
                [
                    {
                        "instruction": "What kind of exercise is good for me?",
                        "is_question": 1,
                    },
                    {
                        "response": "Running",
                        "is_positive": 1,
                    },
                ],
                [
                    {
                        "instruction": "What kind of exercise is good for me?",
                        "is_question": 1,
                    },
                    {
                        "response": "Running",
                        "is_positive": 1,
                    },
                ],
            ],
            verbose=True,
        )

        # DataFrame with "input-" and "output-" prefix columns, matching the types above
        df = pd.DataFrame([
            {
                "input-instruction": "What kind of exercise is good for me?",
                "input-is_question": 1,
                "output-response": "Running",
                "output-is_positive": 1,
            },
            {
                "input-instruction": "What kind of exercise is good for me?",
                "input-is_question": 1,
                "output-response": "Running",
                "output-is_positive": 1,
            },
        ], columns=["input-instruction", "input-is_question", "output-response", "output-is_positive"])
        model.load_data_from_dataframe(df, verbose=True)

        # Two separate dataframes, one for input and one for output
        input_df = pd.DataFrame([
            {
                "instruction": "What kind of exercise is good for me?",
                "is_question": 1,
            },
            {
                "instruction": "What kind of exercise is good for me?",
                "is_question": 1,
            },
        ], columns=["instruction", "is_question"])
        output_df = pd.DataFrame([
            {
                "response": "Running",
                "is_positive": 1,
            },
            {
                "response": "Running",
                "is_positive": 1,
            },
        ], columns=["response", "is_positive"])
        model.load_data_from_paired_dataframes(input_df, output_df, verbose=True)

        # Test loading data from a jsonlines file, two formats
        model.load_data_from_jsonlines("tests/input_output_runner_data_flattened.jsonl", verbose=True)
        model.load_data_from_jsonlines("tests/input_output_runner_data.jsonl", verbose=True)

        model.train()
        print("new model: " + model.model_name)

        # Test 2 types of evaluation
        model.evaluate()
        print(model.evaluation)

        results = model.evaluate()
        print(results)

        # Test single inference
        output = model(Input(instruction="What kind of exercise is OK for me?", is_question=1))
        print(output)

        # Test batch inference
        outputs = model(
            [
                Input(instruction="What kind of exercise is OK for me?", is_question=1),
                Input(instruction="What kind of exercise is so-so for me?", is_question=1),
            ]
        )
        print(outputs)
