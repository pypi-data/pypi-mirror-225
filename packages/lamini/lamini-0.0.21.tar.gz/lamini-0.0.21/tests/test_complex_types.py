from llama import Type, LLMEngine, Context
from typing import List, Dict, Union, Set

# from llama import StringType, DictType, ListType, SetType, IntType, FloatType

import unittest


class TestComplexTypes(unittest.TestCase):
    def test_complex_types(self):
        class Title(Type):
            title: str = Context("title of the story")

        class Body(Type):
            body: str = Context("body of the story")

        class Story2(Type):
            story: Dict[Title, Body] = Context("the whole story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: Tone = Context("tone of the story")

        def write_story(descriptors: Descriptors) -> Story2:
            llm = LLMEngine(id="write_story")
            story = llm(input=descriptors, output_type=Story2)

            return story

        class Note(Type):
            note: str = Context("the note")

        class QuestionAnswerPair(Type):
            question: str = Context("the question")
            answer: str = Context("the answer")

        class QuestionAnswerPairs(Type):
            pairs: List[QuestionAnswerPair] = Context("question answer pairs")

        def get_question_answer_pairs(note: Note) -> QuestionAnswerPairs:
            llm = LLMEngine(id="get_question_answer_pairs")
            question_answer_pairs = QuestionAnswerPairs(
                pairs=[
                    QuestionAnswerPair(
                        question="What is Mendelian?", answer="Complete Dominance."
                    )
                ]
            )
            question_answer_pairs = llm(input=note, output_type=QuestionAnswerPairs)
            return question_answer_pairs

            note = Note(
                note="""- Mendelian = Complete Dominance
            - Only the dominant allele’s protein is produced
            - When a yellow and purple parent produce a purple offspring
        - Not all traits are simply determined by a single dominant and a single recessive allele.  - Incomplete Dominance (see Diana’s picture)
            - A little of each allele’s protein is produced.""",
            )

            question_answer_pairs = get_question_answer_pairs(note=note)

            print(question_answer_pairs)
