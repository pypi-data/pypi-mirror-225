from llama import Type, Context, LLMEngine

import unittest


class GPT4(unittest.TestCase):
    def test_model_name_gpt4(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        llm = LLMEngine(id="test_model_name_cohere", model_name="gpt-4")

        tone = Tone(tone="meme lord")
        story = llm(input=tone, output_type=Story)
        print(story)
