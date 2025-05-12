import json
from langchain.evaluation.qa import QAEvalChain
from langchain.chat_models import ChatOpenAI

# Load evaluation examples
with open("tests/eval_sample.json") as f:
    examples = json.load(f)

predictions = [{"question": e["question"], "answer": e["model_answer"]} for e in examples]

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
eval_chain = QAEvalChain.from_llm(llm)
results = eval_chain.evaluate(examples, predictions)

for result in results:
    print(result)