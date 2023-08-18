from llama import Type, Context, LLMEngine
from inspect import getmembers, getsource, isfunction, ismodule, isclass
import unittest
import llama


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


class TestLLMTrain(unittest.TestCase):
    def test_train_and_cancel(self):
        functions = [make_function(function) for function in get_functions(llama)]
        questions = [
            [
                Question(question="How do I use this function?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ]
        ]
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")
        functions = functions + questions
        llm.save_data(functions)
        job = llm.submit_training_job(verbose=True)
        print(job)
        status = llm.get_training_job_status(job["job_id"])
        print(status)
        all_jobs = llm.list_all_training_jobs()
        print("ALL JOBS")
        print(all_jobs)

        print("Canceling job %s" % job["job_id"])
        response = llm.cancel_training_job(job["job_id"])
        print(response)
        response = llm.cancel_all_training_jobs()
        print(response)

    def test_cancel_nonexistent(self):
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")

        response = llm.cancel_training_job(100000000)
        print(response)

    def test_train(self):
        functions = [make_function(function) for function in get_functions(llama)]
        questions = [
            [
                Question(question="How do I use this function?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ]
        ]
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")
        functions = functions + questions
        llm.save_data(functions)
        eval_results = llm.train(verbose=True)
        print(eval_results)

    def test_train_public(self):
        functions = [make_function(function) for function in get_functions(llama)]
        questions = [
            [
                Question(question="How do I use this function?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ]
        ]
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")
        functions = functions + questions
        llm.save_data(functions)
        eval_results = llm.train(is_public=True, verbose=True)
        print(eval_results)

    def test_train_with_data(self):
        functions = [make_function(function) for function in get_functions(llama)]
        questions = [
            [
                Question(question="How do I use this function?"),
                Answer(
                    inputs=["param1", "param2", "param3"],
                    outputs=["output1", "output2", "output3"],
                    description="This function does something useful",
                ),
            ]
        ]
        llm = LLMEngine(id="QA", model_name="hf-internal-testing/tiny-random-gpt2")
        functions = functions + questions
        eval_results = llm.train(functions, is_public=True, verbose=True)
        print(eval_results)
