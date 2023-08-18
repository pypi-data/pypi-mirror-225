from llama import Lamini
import unittest
from inspect import getmembers, getsource, isfunction, ismodule, isclass
import llama


class TestLaminiEngine(unittest.TestCase):
    def test_inference_simple(self):
        descriptors = {
            "likes": "llamas and other animals",
            "favorite_song": "never let me go",
            "tone": "cheeky",
        }
        out_type = {"story": "a story"}
        llm = Lamini("test", "hf-internal-testing/tiny-random-gpt2")

        story1 = llm(descriptors, out_type)

        print("=====STORY 1======")
        print(story1)
        assert "story" in story1
        assert isinstance(story1["story"], str)

    def test_train(self):
        llm = Lamini("test", "hf-internal-testing/tiny-random-gpt2")
        data = [
            [
                {
                    "likes": "llamas and other animals",
                    "favorite_song": "never let me go",
                    "tone": "cheeky",
                },
                {"story": "a story"},
            ]
            for i in range(10)
        ]
        llm.save_data_pairs(data)
        result = llm.train()

        print(result)
        assert result["status"] == "COMPLETED"

    def test_train_cancel(self):
        llm = Lamini("test", "hf-internal-testing/tiny-random-gpt2")
        data = [
            [
                {
                    "likes": "llamas and other animals",
                    "favorite_song": "never let me go",
                    "tone": "cheeky",
                },
                {"story": "a story"},
            ]
            for i in range(10)
        ]
        llm.save_data_pairs(data)
        job = llm.train_async()

        print("Canceling job %s" % job["job_id"])
        response = llm.cancel_job(job["job_id"])
        print(response)
        assert response["status"] == "CANCELLED"
        assert response["job_id"] == job["job_id"]

    def test_add_and_delete_data(self):
        llm = Lamini("test_add_and_delete_data", "hf-internal-testing/tiny-random-gpt2")
        data = [
            [
                {
                    "likes": "llamas and other animals",
                    "favorite_song": "never let me go",
                    "tone": "cheeky",
                },
                {"story": "a story"},
            ]
            for i in range(10)
        ]
        result1 = llm.save_data_pairs(data)
        print(result1)
        result2 = llm.save_data_pairs(data)
        print(result2)
        assert result1["dataset"] == result2["dataset"]

        seen = set()

        def get_functions(module):
            functions = set()
            if module not in seen:
                seen.add(module)
                for name, member in getmembers(module):
                    if isfunction(member):
                        functions.add((name, getsource(member).strip()))
                    elif ismodule(member) and member.__name__.startswith("llama"):
                        functions.update(get_functions(member))
                    elif (
                        isclass(member)
                        and hasattr(member, "__module__")
                        and f"{member.__module__}.{member.__qualname__}".startswith(
                            "llama"
                        )
                    ):
                        functions.update(get_functions(member))
            return functions

        def make_function(function):
            return {"name": function[0], "code": function[1]}

        functions = [make_function(function) for function in get_functions(llama)]
        llm.save_data(functions)
        result = llm.delete_data("test_add_and_delete_data")
        print(result)
        assert result["deleted"] == 2
