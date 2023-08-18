from llama import Type, Context, LLMEngine

import unittest


class TestMultipleModels(unittest.TestCase):
    def test_multiple_models(self):
        class Story(Type):
            title: str = Context("the title of the story")
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class DetailedDescriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: Tone = Context("tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")

        llm = LLMEngine(id="multiple_models")

        def write_story(descriptors: Descriptors) -> Story:
            story = llm(input=descriptors, output_type=Story)
            return story

        def write_detailed_story(descriptors: DetailedDescriptors) -> Story:
            story = llm(input=descriptors, output_type=Story)
            return story

        descriptors = Descriptors(
            likes="llamas and other animals",
        )

        story = write_story(descriptors)

        print("simple story", story)

        detailed_descriptors = DetailedDescriptors(
            likes="llamas and other animals",
            favorite_song="never let me go",
            tone=Tone(tone="cheeky"),
        )

        story = write_detailed_story(detailed_descriptors)

        print("detailed story", story)
