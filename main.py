import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import spacy
    import en_core_web_sm

    from datasets import load_dataset
    from spacy import displacy


    return displacy, load_dataset, mo


@app.cell
def _(load_dataset):
    dataset = load_dataset("BramVanroy/conll2002", "es")
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
    dataset["train"][index.value]["tokens"]
    return


@app.cell
def _(dataset, displacy, index, mo):
    id2label = {
        0: "O",
        1: "B-PER", 2: "I-PER",
        3: "B-ORG", 4: "I-ORG",
        5: "B-LOC", 6: "I-LOC",
        7: "B-MISC", 8: "I-MISC"
    }
    label2id = {v: k for k, v in id2label.items()}

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


if __name__ == "__main__":
    app.run()
