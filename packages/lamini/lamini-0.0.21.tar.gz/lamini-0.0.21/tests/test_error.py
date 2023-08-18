from llama import Type, Context, LLMEngine
import llama
import unittest


class TestError(unittest.TestCase):
    def test_error(self):
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
        llm = LLMEngine(id="test_error")
        try:
            story1 = llm(input=descriptors, output_type=Story, model_name="Grrr")
        except Exception as e:
            print(e)
            if isinstance(e, llama.error.ModelNameError):
                print(e)
                return True
            else:
                raise e

    def test_download_error(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        descriptors = Descriptors(
            likes="llamas and other animals",
            favorite_song="never let me go",
            tone="cheeky",
        )
        llm = LLMEngine(id="test_error")
        try:
            story1 = llm(
                input=descriptors,
                output_type=Story,
                model_name="EleutherAI/pythia-410m-v0",
            )
        except Exception as e:
            print(e)
            if isinstance(e, llama.error.UnavailableResourceError):
                print(e)
                return True
            else:
                raise e
