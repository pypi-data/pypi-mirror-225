from typing import List
from llama import Type, Context, LLMEngine
import jsonlines
import pandas as pd


# Input
class Question(Type):
    question: str = Context("a question")


# Output
class Answer(Type):
    answer: str = Context("the response to the question")


class QuestionAnswerModel:
    """A class for running and training a question answering model"""

    def __init__(
        self,
        model_name: str = "EleutherAI/pythia-410m-deduped",
        task_name: str = "question_answer_runner_data",
        enable_peft=False,
        config={},
    ):
        self.model_name = model_name
        self.llm = LLMEngine(id=task_name, model_name=model_name, config=config)
        self.question_answer = []
        self.job_id = None
        self.evaluation_results = None
        self.enable_peft = enable_peft

    def get_answer(
        self,
        question: str,
    ) -> str:
        """Get answer to a single question"""
        question_object = Question(question=question)
        answer_object = self.llm(
            input=question_object,
            output_type=Answer,
            model_name=self.model_name,
            task="question_answer",
            enable_peft=self.enable_peft,
        )
        return answer_object.answer

    def get_answers(self, questions: List[str]) -> List[str]:
        """Get answers to a batch of questions"""
        print("Asking %d questions" % len(questions))
        question_objects = [Question(question=q) for q in questions]
        answer_objects = self.llm(
            input=question_objects,
            output_type=Answer,
            model_name=self.model_name,
            task="question_answer",
        )
        answers = [a.answer for a in answer_objects]
        return [{"question": q, "answer": a} for q, a in zip(questions, answers)]

    def load_question_answer(self, data):
        """
        Load a list of json objects with question answer keys into the LLM
        Each object must have 'question' and 'answer' as keys.
        """
        try:
            question_answer_objects = [
                [Question(question=d["question"]), Answer(answer=d["answer"])]
                for d in data
            ]
        except KeyError:
            raise ValueError("Each object must have 'question' and 'answer' as keys")
        self.question_answer.extend(question_answer_objects)

    def load_question_answer_from_jsonlines(self, file_path: str):
        """
        Load a jsonlines file with question answer keys into the LLM.
        Each line must be a json object with 'question' and 'answer' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_question_answer(data)

    def load_question_answer_from_dataframe(self, df: pd.DataFrame):
        """
        Load a pandas dataframe with question answer keys into the LLM.
        Each row must have 'question' as a key.
        """
        try:
            for _, row in df.iterrows():
                self.question_answer.append(
                    [Question(question=row["question"]), Answer(answer=row["answer"])]
                )
        except KeyError:
            raise ValueError("Each object must have 'question' and 'answer' as keys")

    def load_question_answer_from_csv(self, file_path: str):
        """
        Load a csv file with question answer keys into the LLM.
        Each row must have 'question' and 'answer' as keys.
        """
        df = pd.read_csv(file_path)
        self.load_question_answer_from_dataframe(df)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.llm.clear_data()
        self.question_answer = []

    def train(
        self,
        verbose: bool = False,
        finetune_args={},
        enable_peft=None,
        peft_args={},
        limit=500,
        is_public=False,
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if not enable_peft:
            enable_peft = self.enable_peft
        if len(self.question_answer) < 10:
            raise Exception("Submit at least 10 question answer pairs to train")
        if len(self.question_answer) > limit:
            qa_pairs = self.question_answer[:limit]
        else:
            qa_pairs = self.question_answer

        final_status = self.llm.train(
            qa_pairs,
            task="question_answer",
            verbose=verbose,
            finetune_args=finetune_args,
            enable_peft=enable_peft,
            peft_args=peft_args,
            is_public=is_public,
        )
        try:
            self.model_name = final_status["model_name"]
            self.job_id = final_status["job_id"]
            self.llm.clear_data()
        except KeyError:
            raise Exception("Training failed")

        return final_status

    def evaluate(self) -> List:
        """Get evaluation results"""
        self.evaluation_results = self.llm.evaluate()
        return self.evaluation_results

    def get_eval_results(self) -> List:
        if self.job_id is None:
            raise Exception("Must train before getting results (no job id))")
        return self.llm.eval(self.job_id)
