import csv
from difflib import SequenceMatcher


def get_model_files(models, files):
    models_for_import = {}

    for m in models:
        max_w = 0
        file = None
        for p in files:
            if SequenceMatcher(None, p.stem, m).ratio() > max_w:
                file = p
                max_w = SequenceMatcher(None, p.stem, m).ratio()
        if max_w > 0.85:
            models_for_import[file] = models[m]

    return models_for_import


def load_data(file, model, out, err):
    success_count = 0
    line_nr = 0

    with file.open() as f:
        file_content = csv.DictReader(f)
        fields_to_rename = []
        for field in model._meta.get_fields():
            if field.__class__.__name__ in ('ForeignKey',):
                fields_to_rename.append(field.name)

        names = list(file_content.fieldnames)
        for i in range(len(names)):
            if names[i] in fields_to_rename:
                names[i] += '_id'
        file_content.fieldnames = names

        for line in file_content:
            try:
                line_nr += 1
                model.objects.create(**line)
                success_count += 1
            except Exception as e:
                err.write(
                    f'{model.__name__} : {file.name} : line {line_nr}: {e}'
                )
    return success_count
