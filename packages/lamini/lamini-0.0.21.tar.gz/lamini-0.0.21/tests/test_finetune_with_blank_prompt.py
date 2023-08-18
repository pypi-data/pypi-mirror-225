from llama import LLMEngine
import unittest

from llama.prompts.blank_prompt import BlankPrompt


class TestFinetuneCustomPrompts(unittest.TestCase):
    def test_blank_prompt(self):
        prompt = BlankPrompt()
        llm = LLMEngine(
            id="Example",
            prompt=prompt,
            model_name="hf-internal-testing/tiny-random-gpt2",
        )
        print(
            prompt.construct_prompt(
                prompt.input(input="What is the meaning of life?"), prompt.output
            )
        )
        ans = llm(prompt.input(input="What is the meaning of life?"), prompt.output)
        print(ans)

        data = [
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
            [
                prompt.input(input="How do I use this function?"),
                prompt.output(
                    output="This function does something useful",
                ),
            ],
        ]
        llm.save_data(data)

        llm.train()
