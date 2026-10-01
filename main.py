import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import json

    import anthropic
    import marimo as mo
    import spacy
    import en_core_web_sm

    from datasets import load_dataset
    from dotenv import load_dotenv
    from spacy import displacy


    return anthropic, displacy, json, load_dataset, load_dotenv, mo, os


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
    return


@app.cell
def _(anthropic, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    return (client,)


@app.cell
def _(instance):
    " ".join(instance)
    return


app._unparsable_cell(
    r"""
    def tag_with_model(client, sentence, labels)
    """,
    name="_"
)


@app.cell
def _(client, instance):
    message = client.messages.create(
      model="claude-haiku-4-5",
      max_tokens=1024,
      system="In the message, you will be given a sentence. tag the entities in it. Return a json object with the entities and their prefixes and suffixes.",
      messages=[ 
      {
          "role": "user",
          "content": " ".join(instance)
                
      }        
    ]
    )
    for block in message.content:
        if block.type == "text":
            json_text = block.text
            print(block.text)
    return (json_text,)


@app.cell
def _(json, json_text):
    json.loads(json_text[8:-4])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
