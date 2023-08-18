import unittest
from llama.runners.llama_v2_runner import LlamaV2Runner
import json, os

from llama.error.error import UserError

DEFAULT_SYSTEM_PROMPT = """\
You are a Lamini Bot and are designed to answer questions related to Lamini. Lamini is a platform for every developer to build customized, private models: easier, faster, and better-performing than any general purpose LLM. Try to absorb the following information about Lamini in your knowledge base and try to learn about lamini.
"""
PYTHON_SYSTEM_PROMPT = """\
You are a Lamini Bot and are designed to answer questions related to Lamini. Lamini is a platform for every developer to build customized, private models: easier, faster, and better-performing than any general purpose LLM. Try to absorb the following code about Lamini in your knowledge base and try to learn about lamini.
"""
DOC_SYSTEM_PROMPT = """\
You are a Lamini Bot and are designed to answer questions related to Lamini. Lamini is a platform for every developer to build customized, private models: easier, faster, and better-performing than any general purpose LLM. Try to absorb the following data in form of markdown file about Lamini documenation in your knowledge base and try to learn about lamini.
"""


def get_type(file):
    return os.path.splitext(file)[1]


def load_data(path="data/"):
    docs = []
    for root, _, files in os.walk(path):
        for file in files:
            print(file)
            type = get_type(file)
            if type == ".py":
                prompt = PYTHON_SYSTEM_PROMPT
            elif type == ".md":
                prompt = DOC_SYSTEM_PROMPT
            else:
                prompt = DEFAULT_SYSTEM_PROMPT
            if type == ".md" or type == ".txt" or type == ".py":
                doc_path = os.path.join(root, file)
                # print(doc_path)
                with open(doc_path) as doc_file:
                    files = doc_file.read()
                    segments = files.split("\n\n")
                    for segment in segments:
                        docs.append(
                            {
                                "user": segment,
                                "system": prompt,
                                "output": "",
                            }
                        )
    return docs


def load_data_chunk(path="data/"):
    docs = []
    for root, _, files in os.walk(path):
        for file in files:
            print(file)
            type = get_type(file)
            if type == ".py":
                prompt = PYTHON_SYSTEM_PROMPT
            elif type == ".md":
                prompt = DOC_SYSTEM_PROMPT
            else:
                prompt = DEFAULT_SYSTEM_PROMPT
            if type == ".md" or type == ".txt" or type == ".py":
                doc_path = os.path.join(root, file)
                # print(doc_path)
                with open(doc_path) as doc_file:
                    files = doc_file.read()
                    segments = files.split("\n\n")
                    for segment in segments:
                        chunks = [
                            segment[i : i + 20000]
                            for i in range(0, len(segment), 20000)
                        ]
                        for chunk in chunks:
                            docs.append(
                                {
                                    "user": chunk,
                                    "system": prompt,
                                    "output": "",
                                }
                            )
    return docs


class TestLargeDatapoint(unittest.TestCase):
    def test_failed_data(self):
        data = load_data()[:10]

        model = LlamaV2Runner("hf-internal-testing/tiny-random-gpt2")
        model.clear_data()

        try:
            model.load_data(data)
            model.llm.save_data(model.data)
        except Exception as e:
            assert isinstance(e, UserError)

    def test_success_data(self):
        data = load_data_chunk()[:10]

        print(len(data))
        print(len(str(data)))

        model = LlamaV2Runner("hf-internal-testing/tiny-random-gpt2")
        model.clear_data()
        model.load_data(data)
        model.llm.submit_training_job(model.data, finetune_args={"max_steps": 10})
        model.llm.cancel_training_job(model.job_id)
