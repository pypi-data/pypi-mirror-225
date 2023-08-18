from llama import Type, Context, LLMEngine

import llama
from multi_model_test import MultiModelTest
from multi_model_test import run_models


class TestParallel(MultiModelTest):
    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_parallel_complex(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        # llm = LLMEngine(id="output_str")

        # future changes to remove this decorator
        @self.llm.parallel
        def circular_operation(descriptor: Descriptor) -> Descriptor:
            story = self.llm.add_model(input=descriptor, output_type=Story)
            descriptor = self.llm.add_model(input=story, output_type=Descriptor)
            return descriptor

        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        descriptors = [circular_operation(descriptor) for descriptor in descriptors]
        llama.run_all(descriptors)

    @run_models(models=["hf-internal-testing/tiny-random-gpt2", "text-davinci-003"])
    def test_parallel_simple(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        # self.llm = LLMEngine(id="output_str")
        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        self.llm.add_data(
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky100",
            )
        )
        stories = [
            self.llm.add_model(input=descriptor, output_type=Story)
            for descriptor in descriptors
        ]
        llama.run_all(stories)

    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_parallel_super_simple(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Descriptor(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: str = Context("tone of the story")

        # self.llm = LLMEngine(id="output_str")
        descriptors = [
            Descriptor(
                likes="llamas and other animals4c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals2b",
                favorite_song="never let me go",
                tone="cheeky",
            ),
            Descriptor(
                likes="llamas and other animals3c",
                favorite_song="never let me go",
                tone="cheeky",
            ),
        ]
        self.llm.add_data(
            Descriptor(
                likes="llamas and other animals1a",
                favorite_song="never let me go",
                tone="cheeky100",
            )
        )
        stories = self.llm(descriptors, output_type=Story)
        print(stories)
