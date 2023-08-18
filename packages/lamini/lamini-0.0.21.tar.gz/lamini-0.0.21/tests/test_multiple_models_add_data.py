from llama import Type, Context, LLMEngine

import unittest

from llama import Type, Context
from typing import List

import llama


class TestMultipleModelsAddData(unittest.TestCase):
    def test_multiple_models_add_data(self):
        class Turn(Type):
            speaker: str = Context("the speaker in the conversation, either CX or AI")
            text: str = Context("the words spoken by the speaker")

        class Conversation(Type):
            turns: List[Turn] = Context("the conversation")

        class Order(Type):
            menu_item: str = Context("the name of the item on the menu")
            count: int = Context("the number of items ordered")

        class ASRError(Type):
            error_text: str = Context(
                "the words that were not transcribed correctly by the automatic speech recognition system"
            )
            contains_error: int = Context(
                "1 if this trascript contain a speech recognition error, otherwise 0"
            )

        def get_del_taco_data():
            return [
                Conversation(
                    turns=[
                        Turn(speaker="CX", text="Do you have the Del Taco?"),
                        Turn(speaker="AI", text="Yes we do."),
                        Turn(speaker="CX", text="Can I have the Del Taco?"),
                        Turn(speaker="AI", text="Sure. What kind of meat?"),
                        Turn(speaker="CX", text="Chicken."),
                        Turn(speaker="AI", text="<readback>"),
                    ]
                ),
                Order(menu_item="Del Taco", count=1),
            ]

        llm = LLMEngine(id="multiple_models_add_data")

        example_conversation = Conversation(
            turns=[
                Turn(speaker="CX", text="Do you have the Del Taco?"),
                Turn(speaker="AI", text="Yes we do."),
                Turn(speaker="CX", text="Can I have the Del Taco?"),
                Turn(speaker="AI", text="Sure. What kind of meat?"),
                Turn(speaker="CX", text="Chicken."),
                Turn(speaker="AI", text="<readback>"),
            ]
        )

        item = llm(example_conversation, output_type=Order)
        print(item)

        llm.add_data(get_del_taco_data())

        item = llm(example_conversation, output_type=Order)
        print(item)

        error = llm(example_conversation, output_type=ASRError)
        print(error)

        orders = [
            llm.add_model(
                Order(count=i, menu_item="Del Taco", random=True),
                output_type=Conversation,
            )
            for i in range(5)
        ]
        orders = llama.run_all(orders)
        for order in orders:
            print(order)
