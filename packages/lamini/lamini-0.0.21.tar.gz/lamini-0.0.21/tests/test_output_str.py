from llama import Type, Context, LLMEngine

import unittest


class TestOutputStr(unittest.TestCase):
    def test_output_str(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: Tone = Context("tone of the story")

        llm = LLMEngine(id="output_str")

        def write_story(descriptors: Descriptors) -> Story:
            story = llm(input=descriptors, output_type=Story)

            return story

        descriptors = Descriptors(
            likes="llamas and other animals",
            favorite_song="never let me go",
            tone=Tone(tone="cheeky"),
        )

        story = write_story(descriptors=descriptors)

        print(story)
