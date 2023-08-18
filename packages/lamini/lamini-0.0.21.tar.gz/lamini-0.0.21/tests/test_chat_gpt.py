from llama import Type, Context, LLMEngine
import unittest
import time


class ChatGPT(unittest.TestCase):
    def test_model_name_chat_gpt(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        llm = LLMEngine(id="test_model_name_chat_gpt", model_name="chat/gpt-3.5-turbo")

        tone = Tone(tone="meme lord")
        story = llm(input=tone, output_type=Story)
        print(story)
