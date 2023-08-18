from llama import QuestionAnswerModel

data = [
    {"question": "What kind of exercise is good for me?", "answer": "Running"},
    {"question": "hello", "answer": "hello"},
    {"question": "What is the best way to get fit?", "answer": "Running"},
    {"question": "tell me something", "answer": "eat and stay healthy"},
    {"question": "Hey", "answer": "Hey"},
    {"question": "Whats your name?", "answer": "My name is Llama"},
    {"question": "What is the best way to get fit?", "answer": "Running"},
    {"question": "What kind of exercise is good for me?", "answer": "Running"},
    {"question": "What is the best way to get fit?", "answer": "Running"},
    {"question": "What kind of exercise is good for me?", "answer": "Running"}
]
model = QuestionAnswerModel("hf-internal-testing/tiny-random-gpt2")
model.load_question_answer(data)
model.train()
print("new model: " + model.model_name)
# results = model.get_eval_results()
# print(results)
answer = model.get_answer("What kind of exercise is good for me?")
print(answer)


print("Running finetuning on finetuned model")
model1 = QuestionAnswerModel(model.model_name)
model1.load_question_answer(data)
model1.train()
print("new model: " + model1.model_name)
# results = model.get_eval_results()
# print(results)
answer = model1.get_answer("What kind of exercise is good for me?")
print(answer)

print("Running finetuning on finetuned model which was finetuned on finetuned model")
model2 = QuestionAnswerModel(model1.model_name)
model2.load_question_answer(data)
model2.train()
print("new model: " + model2.model_name)
# results = model.get_eval_results()
# print(results)
answer = model2.get_answer("What kind of exercise is good for me?")
print(answer)