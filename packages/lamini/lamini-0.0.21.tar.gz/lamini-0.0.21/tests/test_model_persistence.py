from llama import Type, Context, LLMEngine
from inspect import getmembers, getsource, isfunction, ismodule, isclass
import unittest
import llama
import time


# Input
class Question(Type):
    question: str = Context("question about the function")


# Output
class Answer(Type):
    inputs: list = Context("list of inputs to the function")
    outputs: list = Context("list of outputs from the function")
    description: str = Context("function description in 2 to 5 lines")


class Function(Type):
    name: str = Context("name of the function")
    code: str = Context("text for the python code in the function")


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
                and f"{member.__module__}.{member.__qualname__}".startswith("llama")
            ):
                functions.update(get_functions(member))
    return functions


def make_function(function):
    return Function(name=function[0], code=function[1])


class TestModelPersistence(unittest.TestCase):
    def test_model_persistence(self):
        functions = [make_function(function) for function in get_functions(llama)]

        llm = LLMEngine(
            id="test_tulika", model_name="hf-internal-testing/tiny-random-gpt2"
        )

        qa_data = [
            [
                Question(question="What is the LLM class?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This class handles LLM related stuff",
                ),
            ],
            [
                Question(question="What does add_data do?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ],
        ]
        response = llm.cancel_all_training_jobs()
        print(response)
        llm.clear_data()
        llm.save_data(functions)
        llm.save_data(qa_data)
        job = llm.submit_training_job(task="question_answer")
        print(job)
        status = llm.get_training_job_status(job["job_id"])
        assert status["status"] not in ("FAILED", "CANCELLED")
        while status["status"] != "COMPLETED":
            print(f"job not done. waiting... {status}")
            time.sleep(10)
            status = llm.get_training_job_status(job["job_id"])
            assert status["status"] not in ("FAILED", "CANCELLED")
        print(
            f"Finetuning process completed, model identifier is: {status['model_name']}"
        )
