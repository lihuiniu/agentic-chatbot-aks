import workflow
from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.metrics import(
    faithfulness,
    answer_relevancy,
    contect_precision,
    contect_recall
)

from tests.offline_eval import predictions

#Initialize RAGAS evaluator
evaluator = RagasEvaluatorChain(
    metrics=[
        faithfulness,
        answer_relevancy,
        contect_precision,
        contect_recall
    ]
)
# Define evaluation examples
examples =[
    {
        "question": "How do I reset my Azure login credentials since I already failed maximum retry allowed?",
        "ground_truth": "To reset your Azure login credentials, go to the Azure portal and follow the password reset instructions."
    }
]
#Evaluate each example:
for example in examples:
    result = workflow.invoke({"question": example["question"]})
    evaluation = evaluator.evaluate_run(
        inputs = {"question": example["question"]},
        prediction = {"answer": result},
        reference = {"answer": example["ground_truth"]}
    )
    print(f"Evaluation for question: {example['question']}")
    print(evaluation)
