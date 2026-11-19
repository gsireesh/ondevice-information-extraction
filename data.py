from datasets import load_dataset
from datatypes import gen_Dataset


def load_data(dataset_name: str, split: str, subset: str | None) -> gen_Dataset:
    raw = load_dataset(dataset_name, name=subset, split=split)
    label_names = raw.features["ner_tags"].feature.names

    tokens = []
    true_tags = []

    for row in raw:
        tokens.append(row["tokens"])
        tag_strings = [label_names[tag_id] for tag_id in row["ner_tags"]]
        true_tags.append(tag_strings)

    used_labels = sorted({tag for seq in true_tags for tag in seq})
    id2label = {i: name for i, name in enumerate(used_labels)}
    label2id = {name: i for i, name in enumerate(used_labels)}

    return gen_Dataset(
        tokens=tokens,
        true_tags=true_tags,
        label2id=label2id,
        id2label=id2label
    )
