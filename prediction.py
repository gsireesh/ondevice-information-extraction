
import os
import json
import dspy
import anthropic
from dotenv import load_dotenv
from datatypes import gen_Dataset, PredictionResult


load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

#LLM model
client = anthropic.Anthropic(api_key=api_key)
def tag_with_model(sentence, labels):

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system='In the message, you will be given a sentence. Tag the entities in it. Return a json object with this format: {"entities": [{"entity": "word", "type": "tag", "prefix": "word before", "suffix": "word after"}]}',
        messages=[ 
            {
                "role": "user",
                "content": f"Sentence: {sentence}\nLabels: {labels}"
            }        
        ]
    )
    json_text = None

    for block in message.content:
        if block.type == "text":
            json_text = block.text
            print(block.text)
    return json.loads(json_text[8:-4])

#DSPy model
class ExtractEvent(dspy.Signature):
    """Extract entities from the sentence using the provided allowed labels. Return a json object with this format:
        {"entities": [{"entity": "word", "type": "tag", "prefix": "word before", "suffix": "word after"}]}"""

    sentence = dspy.InputField(desc="The sentence to tag")
    labels = dspy.InputField(desc="The labels you must use")
    json_output = dspy.OutputField(desc="raw JSON output containing entities")

dspy.configure(lm=dspy.LM("anthropic/claude-haiku-4-5"))
tag_generator = dspy.Predict(ExtractEvent)

def tag_with_dspy(sentence, label):

    result = tag_generator(sentence=sentence, labels=label)

    return json.loads(result.json_output)

#models
PREDICTION_MODELS = {
    "dspy": tag_with_dspy,
    "llm": tag_with_model
    #add more later
}

def prediction(data: gen_Dataset, model: str) -> PredictionResult:
    tag_fn = PREDICTION_MODELS[model]
    allowed_labels = str(list(data.label2id.keys()))
    y_pred = []

    for token in data.tokens:
        pred_tags = ["O"] * len(token)

        sentence = " ".join(token)
        entities = tag_fn(sentence, allowed_labels)
        output = entities.get("entities", [])
        lower_tokens = [t.lower() for t in token]

        for item in output:
            entity_text = item["entity"]
            label = item["type"]

            entity_tokens = entity_text.split()
            lower_entity = [t.lower() for t in entity_tokens]
            base_label = label[2:] if label.startswith(("B-", "I-")) else label

            for j in range(len(token)):
                if lower_tokens[j:j+len(entity_tokens)] == lower_entity:
                    pred_tags[j] = f"B-{base_label}"

                    base_label = label[2:] if label.startswith("B-") else label
                    for k in range(1, len(entity_tokens)):
                        pred_tags[j+k] = f"I-{base_label}"
                    break

        y_pred.append(pred_tags)
    
    return PredictionResult(y_true=data.true_tags, y_pred=y_pred)