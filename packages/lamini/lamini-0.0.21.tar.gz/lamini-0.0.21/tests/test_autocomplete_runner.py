from llama import AutocompleteRunner, Type, Context
import unittest
import pandas as pd

class TestAutocompleteRunner(unittest.TestCase):
    def test_autocomplete_runner(self):
        print("Testing AutocompleteRunner...")

        class Text(Type):
            some_cool_text: str = Context("cool text")
            text: str = Context("textttt")
        
        class JustText(Type):
            text: str = Context("text, that's it")

        model = AutocompleteRunner(model_name="hf-internal-testing/tiny-random-gpt2")

        model.load_data(Text(some_cool_text="cool text about lorem ipsum", text="have you tried ipsum lorem tho"), verbose=True)
        model.load_data([JustText(text="yes it's just text but pretty cool"), Text(some_cool_text="cool text about lorem ipsum", text="have you tried ipsum lorem tho")], verbose=True)

        model.load_data_from_strings(["cool text about lorem ipsum", "super cool"], verbose=True)

        model.load_data_from_dataframe(pd.DataFrame([{"text": "cool text about lorem ipsum", "other text": "cool cool"}, {"text": "super cool", "other text": "yes yes yes"}]), verbose=True)
        model.load_data_from_dataframe(pd.DataFrame([{"text": "cool text about lorem ipsum", "not cool": "NO NO NO"}, {"text": "super cool", "not cool": "NO NO NO"}]), columns=["text"], verbose=True)

        # Test loading data from a (flat-only) jsonlines file
        model.load_data_from_jsonlines("tests/input_output_runner_data_flattened.jsonl", keys=["input-instruction", "output-response"], verbose=True)
        

        model.train()
        print("new model: " + model.model_name)

        model.evaluate()
        print(model.evaluation)
        
        print(model.evaluate_autocomplete("cool text about lorem ipsum"))
        print(model.evaluate_autocomplete(["cool text about lorem ipsum", "super cool"]))

        # Test single inference
        output = model("lore")
        print(output)

        # Test batch inference
        outputs = model(["lorem ips", "super"])
        print(outputs)
