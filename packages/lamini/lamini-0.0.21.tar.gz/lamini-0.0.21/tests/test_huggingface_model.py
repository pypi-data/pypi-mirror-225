from llama import Type, Context, LLMEngine
import unittest
import time


class TestHuggingfaceModel(unittest.TestCase):
    def test_model_simple(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        llm = LLMEngine(
            id="test_model_name_chat_gpt",
            model_name="hf-internal-testing/tiny-random-gpt2",
        )

        tone = Tone(tone="meme lord")
        story = llm(input=tone, output_type=Story)
        print(story)
