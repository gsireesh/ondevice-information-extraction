import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from dataclasses import asdict
    from seqeval.metrics import f1_score, precision_score, recall_score

    from datatypes import PredictionResult, EvalMetric
    from data import load_data
    from prediction import prediction

    def compute_metric(result: PredictionResult) -> EvalMetric:
        return EvalMetric(
            f1=f1_score(result.y_true, result.y_pred),
            precision=precision_score(result.y_true, result.y_pred),
            recall=recall_score(result.y_true, result.y_pred)
        )

    def evaluate(model_name: str, dataset_name: str, split: str, subset: str | None) -> EvalMetric:
        data = load_data(dataset_name, subset=subset, split=split)
        pred_result = prediction(data, model=model_name)
        return compute_metric(pred_result)

    if __name__ == "__main__":
        print(evaluate("dspy", "DFKI-SLT/cross_ner", split="test[:5]", subset="conll2003"))
    return


if __name__ == "__main__":
    app.run()
