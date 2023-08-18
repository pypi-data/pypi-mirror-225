from llama import Type, Context

from multi_model_test import MultiModelTest
from multi_model_test import run_models


class TestRandom(MultiModelTest):
    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_random(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: Tone = Context("tone of the story")

        descriptors = Descriptors(
            likes="llamas and other animals",
            favorite_song="never let me go",
            tone=Tone(tone="cheeky"),
        )

        story1 = self.llm(input=descriptors, output_type=Story, random=True)
        story2 = self.llm(input=descriptors, output_type=Story, random=True)

        print(type(story1), type(story2))
        print("=====STORY 1======")
        print(story1)
        print("=====STORY 2======")
        print(story2)

        assert story1 != story2, "Not randomizing"
