import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import json

    import dspy
    import anthropic
    import marimo as mo
    import spacy
    import en_core_web_sm
    import seqeval.metrics

    from datasets import load_dataset
    from dotenv import load_dotenv
    from spacy import displacy

    from seqeval.metrics import accuracy_score
    from seqeval.metrics import classification_report
    from seqeval.metrics import f1_score
    from seqeval.metrics import recall_score
    from seqeval.metrics import precision_score

    return (
        anthropic,
        displacy,
        dspy,
        f1_score,
        json,
        load_dataset,
        load_dotenv,
        mo,
        os,
        precision_score,
        recall_score,
    )


@app.cell
def _(load_dotenv, os):
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return (api_key,)


@app.cell
def _(load_dataset):
    dataset = load_dataset("DFKI-SLT/cross_ner", "conll2003")
    return (dataset,)


@app.cell
def _(dataset):
    dataset
    return


@app.cell
def _(dataset, mo):
    index = mo.ui.slider(start=0, stop=len(dataset["train"]), include_input=True)
    index
    return (index,)


@app.cell
def _(dataset, index):
    instance = dataset["train"][index.value]["tokens"]
    instance
    return (instance,)


@app.cell
def _(dataset, displacy, index, mo):
    label2id = {"O": 0, "B-academicjournal": 1, "I-academicjournal": 2, "B-album": 3, "I-album": 4, "B-algorithm": 5, "I-algorithm": 6, "B-astronomicalobject": 7, "I-astronomicalobject": 8, "B-award": 9, "I-award": 10, "B-band": 11, "I-band": 12, "B-book": 13, "I-book": 14, "B-chemicalcompound": 15, "I-chemicalcompound": 16, "B-chemicalelement": 17, "I-chemicalelement": 18, "B-conference": 19, "I-conference": 20, "B-country": 21, "I-country": 22, "B-discipline": 23, "I-discipline": 24, "B-election": 25, "I-election": 26, "B-enzyme": 27, "I-enzyme": 28, "B-event": 29, "I-event": 30, "B-field": 31, "I-field": 32, "B-literarygenre": 33, "I-literarygenre": 34, "B-location": 35, "I-location": 36, "B-magazine": 37, "I-magazine": 38, "B-metrics": 39, "I-metrics": 40, "B-misc": 41, "I-misc": 42, "B-musicalartist": 43, "I-musicalartist": 44, "B-musicalinstrument": 45, "I-musicalinstrument": 46, "B-musicgenre": 47, "I-musicgenre": 48, "B-organisation": 49, "I-organisation": 50, "B-person": 51, "I-person": 52, "B-poem": 53, "I-poem": 54, "B-politicalparty": 55, "I-politicalparty": 56, "B-politician": 57, "I-politician": 58, "B-product": 59, "I-product": 60, "B-programlang": 61, "I-programlang": 62, "B-protein": 63, "I-protein": 64, "B-researcher": 65, "I-researcher": 66, "B-scientist": 67, "I-scientist": 68, "B-song": 69, "I-song": 70, "B-task": 71, "I-task": 72, "B-theory": 73, "I-theory": 74, "B-university": 75, "I-university": 76, "B-writer": 77, "I-writer": 78}

    id2label = {v: k for k, v in label2id.items()}

    def render(instance):


        tokens = instance["tokens"]
        tag_ids = [id2label[tag_id] for tag_id in instance["ner_tags"]]

        current_char = 0;
        start_char = None;
        current_label = None;

        sentence = ""
        ent = []

        for token, tag_str in zip(tokens, tag_ids):
            word_start = current_char
            word_end = current_char + len(token)

            if (tag_str == "O"):
                if (start_char != None):
                    ent.append({"start": start_char, "end": word_start - 1, "label": current_label})
                    start_char = None;
            elif (tag_str.startswith("B-")):
                if (start_char != None):
                    ent.append({"start": start_char, "end": word_start - 1, "label": current_label})
                start_char = word_start;
                current_label = tag_str[2:]
            elif (tag_str.startswith("I-")):
                pass
            sentence += token + " "
            current_char = word_end + 1

        if (start_char != None):
            ent.append({"start": start_char, "end": current_char - 1, "label": current_label})

        ex = [{"text": sentence,
               "ents": ent,
               "title": None}]

        html_out = displacy.render(ex, style="ent", manual=True)
        return mo.Html(html_out)



    render(dataset["train"][index.value])
    return (label2id,)


@app.cell
def _(anthropic, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    return


@app.cell
def _(instance):
    sentence = " ".join(instance)
    return (sentence,)


@app.cell
def _(json):
    def tag_with_model(client, sentence, labels):

        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system="In the message, you will be given a sentence. tag the entities in it. Return a json object with the entities and their prefixes and suffixes.",
            messages=[ 
                {
                    "role": "user",
                    "content": sentence
                }        
            ]
        )
        json_text = None

        for block in message.content:
            if block.type == "text":
                json_text = block.text
                print(block.text)
        return json.loads(json_text[8:-4])


    return


@app.cell
def _():
    #entities = tag_with_model(client, sentence, label2id)
    #json.loads(json_text[8:-4])
    return


@app.cell
def _(displacy, mo):
    def renderjson(instance, entities):


        tokens = instance["tokens"]
        sentence = " ".join(tokens)
        ent = []
        output = entities.get("entities", [])

        for item in output:
            entity_text = item["entity"]
            label = item["type"]
            before = item["prefix"]
            after = item["suffix"]

            phrase_part = []
            if before:
                phrase_part.append(before)
            phrase_part.append(entity_text)
            if after:
                phrase_part.append(after)

            phrase = " ".join(phrase_part)
            start = sentence.find(phrase)


            if (start != -1):
                if (before):
                    start_char = start + len(before) + 1
                else:
                    start_char = start
                end_char = start_char + len(entity_text)

                if (label.startswith("B-")):
                    clean_label = label[2:]
                else:
                    clean_label = label
    
                ent.append({"start": start_char, "end": end_char, "label": clean_label})


        ex = [{"text": sentence,
               "ents": ent,
               "title": None}]

        html_out = displacy.render(ex, style="ent", manual=True)
        return mo.Html(html_out)

    return (renderjson,)


@app.cell
def _():
    #renderjson(dataset["train"][index.value], entities)
    return


@app.cell
def _(dspy, json, label2id, sentence):
    class ExtractEvent(dspy.Signature):
        """Extract entities from the sentence using the provided allowed labels. Return a json object with this format:
            {"entities": [{"entity": "word", "type": "tag", "prefix": "word before", "suffix": "word after"}]}"""

        sentence = dspy.InputField(desc="The sentence to tag")
        labels = dspy.InputField(desc="The labels you must use")
        json_output = dspy.OutputField(desc="raw JSON output containing entities")

    def tag_with_dspy(sentence, label):
        dspy.configure(lm=dspy.LM("anthropic/claude-haiku-4-5"))

        tag_generator = dspy.Predict(ExtractEvent)
        result = tag_generator(sentence=sentence, labels=label)

        return json.loads(result.json_output)


    tag_with_dspy(sentence, label2id)
    return (tag_with_dspy,)


@app.cell
def _(dataset, index, label2id, renderjson, sentence, tag_with_dspy):
    entities = tag_with_dspy(sentence, label2id)
    renderjson(dataset["train"][index.value], entities)
    return


@app.cell
def _(f1_score, label2id, precision_score, recall_score, tag_with_dspy):
    def calculate(dataset):
        y_true = []
        y_pred = []
        id2label = {v: k for k, v in label2id.items()}
        for i in range(dataset["train"].num_rows):
            items = []
            token = dataset["train"][i]["tokens"]
            true_id = dataset["train"][i]["ner_tags"]

            true_tags = [id2label[tag_id] for tag_id in true_id]
            y_true.append(true_tags)
            pred_tags = ["O"] * len(token)

            sentence = " ".join(token)
            entities = tag_with_dspy(sentence, label2id)
            output = entities.get("entities", [])

            for item in output:
                entity_text = item["entity"]
                label = item["type"]

                entity_tokens = entity_text.split()

                for j in range(len(token)):
                    if token[j:j+len(entity_tokens)] == entity_tokens:
                        pred_tags[j] = label

                        base_label = label[2:] if label.startswith("B-") else label
                        for k in range(1, len(entity_tokens)):
                            pred_tags[j+k] = f"I-{base_label}"
                        break

            y_pred.append(pred_tags)
        print(f1_score(y_true, y_pred)) 
        print(recall_score(y_true, y_pred))
        print(precision_score(y_true, y_pred))
        return y_true, y_pred

    return (calculate,)


@app.cell
def _(calculate, dataset):
    calculate(dataset)
    return


if __name__ == "__main__":
    app.run()
