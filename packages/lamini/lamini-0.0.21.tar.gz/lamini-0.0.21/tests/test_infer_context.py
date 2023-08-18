from llama import Type, Context, LLMEngine

import unittest


class TestInferContext(unittest.TestCase):
    def test_infer_context(self):
        class Tone(Type):
            tone_sub: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: list = Context("things you like")
            tone_desc: Tone

        llm = LLMEngine(id="infer_context")

        tone = Tone(tone_sub="cheeky")
        print("TONE")
        print(tone)
        print(tone.schema())
        descriptors = Descriptors(
            likes=["llamas", "sheep"],
            tone_desc=tone,
        )
        print("DESCRIPTORS")
        print(descriptors)
        print(descriptors.schema())

        print("LLAMA")
        tone = llm(input=descriptors, output_type=Tone)
        print(tone)
