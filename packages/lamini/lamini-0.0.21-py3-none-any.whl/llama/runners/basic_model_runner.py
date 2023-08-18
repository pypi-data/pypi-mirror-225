from typing import List, Union
from llama import Type, Context, LLMEngine
import jsonlines
import pandas as pd

from llama.prompts.blank_prompt import BlankPrompt


class Input(Type):
    input: str = Context(" ")


class Output(Type):
    output: str = Context(" ")


class BasicModelRunner:
    """A class for running and training a model with a blank prompt (string in, string out)"""

    def __init__(
        self,
        model_name: str = "EleutherAI/pythia-410m-deduped",
        enable_peft=False,
        config={},
    ):
        self.model_name = model_name
        self.prompt = BlankPrompt()
        self.llm = LLMEngine(
            "basic_model_runner_data",
            model_name=model_name,
            config=config,
            prompt=self.prompt,
        )
        self.job_id = None
        self.data = []
        self.evaluation = None
        self.enable_peft = enable_peft

    def __call__(self, inputs: Union[str, List[str]]) -> str:
        """Call the model runner on prompt"""
        # Alternative way to run it:
        # output = self.llm(self.prompt.input(input=input_string), self.prompt.output)

        if isinstance(inputs, list):
            print("Running batch job on %d number of inputs" % len(inputs))
            input_objects = [Input(input=i) for i in inputs]
        else:
            # Singleton
            input_objects = Input(input=inputs)
        output_objects = self.llm(
            input=input_objects,
            output_type=Output,
            model_name=self.model_name,
            enable_peft=self.enable_peft,
        )
        if isinstance(output_objects, list):
            outputs = [o.output for o in output_objects]
            return [{"input": i, "output": o} for i, o in zip(inputs, outputs)]
        else:
            return output_objects.output

    def get_keys(self, data_keys):
        if "question" in data_keys and "answer" in data_keys:
            keys = ["question", "answer"]
        elif "instruction" in data_keys and "response" in data_keys:
            keys = ["instruction", "response"]
        elif "input" in data_keys and "output" in data_keys:
            keys = ["input", "output"]
        else:
            keys = ["text", None]
        return keys

    def load_data(self, data, verbose: bool = False):
        """
        Load a list of json objects with input-output keys into the LLM
        Each object must have 'input' and 'output' as keys.
        """
        # Get keys
        if not isinstance(data, list) and not isinstance(data[0], dict):
            raise ValueError(
                "Data must be a list of dicts with keys 'input' and 'output'"
            )

        data_keys = data[0].keys()
        keys = self.get_keys(data_keys)

        try:
            input_output_objects = [
                [
                    Input(input=d[keys[0]]),
                    Output(output=d[keys[1]]) if keys[1] else Output(output=""),
                ]
                for d in data
            ]
        except KeyError:
            raise ValueError("Each object must have 'input' and 'output' as keys")
        self.data.extend(input_output_objects)
        if verbose:
            print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_jsonlines(self, file_path: str, verbose: bool = False):
        """
        Load a jsonlines file with input output keys into the LLM.
        Each line must be a json object with 'input' and 'output' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_data(data, verbose=verbose)

    def load_data_from_dataframe(self, df: pd.DataFrame, verbose: bool = False):
        """
        Load a pandas dataframe with input output keys into the LLM.
        Each row must have 'input' and 'output' as keys.
        """
        data_keys = df.columns
        keys = self.get_keys(data_keys)

        input_output_objects = []
        try:
            for _, row in df.iterrows():
                input_output_objects.append(
                    [
                        Input(input=row[keys[0]]),
                        Output(output=row[keys[1]]) if keys[1] else Output(output=""),
                    ]
                )
        except KeyError:
            raise ValueError("Each object must have 'input' and 'output' as keys")
        self.data.extend(input_output_objects)

        if verbose:
            print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_csv(self, file_path: str, verbose: bool = False):
        """
        Load a csv file with input output keys into the LLM.
        Each row must have 'input' and 'output' as keys.
        """
        df = pd.read_csv(file_path)
        self.load_data_from_dataframe(df, verbose=verbose)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.llm.clear_data()
        self.data = []

    def train(
        self, verbose: bool = False, finetune_args={}, limit=500, is_public=False
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if len(self.data) < 10:
            raise Exception("Submit at least 10 data pairs to train")
        if len(self.data) > limit:
            data = self.data[:limit]
        else:
            data = self.data

        final_status = self.llm.train(
            data, verbose=verbose, finetune_args=finetune_args, is_public=is_public
        )
        try:
            self.model_name = final_status["model_name"]
            self.job_id = final_status["job_id"]
            self.llm.clear_data()
        except KeyError:
            raise Exception("Training failed")

    def evaluate(self) -> List:
        """Get evaluation results"""
        self.evaluation = self.llm.evaluate()
        return self.evaluation

    def get_eval_results(self) -> List:
        if self.job_id is None:
            raise Exception("Must train before getting results (no job id))")
        self.evaluation = self.llm.eval(self.job_id)
        return self.evaluation
