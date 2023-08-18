from llama import LLMEngine, Type, Context
import unittest

from llama.program.util.config import edit_config, get_config
from llama.program.util.run_ai import get_url_and_key
from llama.program.util.config import reset_config
from llama.prompts.general_prompt import GeneralPrompt
from llama.prompts.qa_prompt import QAPrompt
from llama.prompts.blank_prompt import BlankPrompt
from llama.prompts.llama_v2_prompt import LlamaV2Prompt, LlamaV2Input, LlamaV2Output


# Input
class UserQuestion(Type):
    chat_history: str = Context("chat history")
    question: str = Context("question about ifit")
    user_info: str = Context("information about the user asking the question")


# Output
class ModelAnswer(Type):
    answer: str = Context("Response from the model")


# Output
class UserData(Type):
    height: str = Context("user height")
    age: str = Context("user age")
    weight: str = Context("user weight")


# Input
class Recommendation(Type):
    recommendation_url: str = Context("Link to a workout")
    user_info: UserData = Context("information about the user")


# Output
class Message(Type):
    message: str = Context("message to the user containing a recommendation")


class Question(Type):
    question: str = Context("question about the function")


class Answer(Type):
    answer: str = Context("Response from the model")


class TestCustomPrompts(unittest.TestCase):
    def test_general_prompt(self):
        prompt = GeneralPrompt()

        hydrated_prompt = prompt.construct_prompt(
            input=Question(question="What is the meaning of life?"), output_type=Answer
        )
        print(hydrated_prompt)
        llm = LLMEngine(
            id="test", prompt=prompt, model_name="hf-internal-testing/tiny-random-gpt2"
        )
        ans = llm(
            input=Question(question="What is the meaning of life?"), output_type=Answer
        )
        print(ans)

    def test_qa_prompt(self):
        prompt = QAPrompt()

        hydrated_prompt = prompt.construct_prompt(
            input=Question(question="What is the meaning of life?"), output_type=Answer
        )
        print(hydrated_prompt)
        llm = LLMEngine(
            id="test", prompt=prompt, model_name="hf-internal-testing/tiny-random-gpt2"
        )
        ans = llm(
            input=Question(question="What is the meaning of life?"), output_type=Answer
        )
        print(ans)

    def test_blank_prompt(self):
        prompt = BlankPrompt()
        llm = LLMEngine(
            id="Example",
            prompt=prompt,
            model_name="hf-internal-testing/tiny-random-gpt2",
        )
        ans = llm(prompt.input(input="What is the meaning of life?"), prompt.output)
        print(ans)

    def test_custom_prompt(self):
        prompt = LlamaV2Prompt()
        llm = LLMEngine(
            id="Example",
            prompt=prompt,
            model_name="hf-internal-testing/tiny-random-gpt2",
        )
        ans = llm(
            LlamaV2Input(
                user="What is the meaning of life?", system="Speak like a pirate."
            ),
            LlamaV2Output,
        )
        print(ans)
