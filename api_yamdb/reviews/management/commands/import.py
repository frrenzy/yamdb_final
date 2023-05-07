from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ._utils import get_model_files, load_data


class Command(BaseCommand):
    help = 'Imports data from static/data into project tables'

    def add_arguments(self, parser):
        parser.add_argument('model_name', nargs='+', type=str)

    def handle(self, *args, **options):
        models = dict(apps.all_models['reviews'])
        models.update(dict(apps.all_models['users']))

        models_for_import = {}

        try:
            for model_name in options['model_name']:
                model = models[model_name.lower()]
                models_for_import[model_name.lower()] = model
        except KeyError:
            self.stderr.write(
                self.style.ERROR(f'model {model_name} does not exist')
            )

        if len(models_for_import.keys()) == 0:
            raise CommandError('Models for import are not found')

        self.stdout.write(', '.join(models_for_import.keys()))

        path = settings.BASE_DIR / 'static' / 'data'
        files = [p for p in path.iterdir() if p.is_file()]

        files_models = get_model_files(models_for_import, files)

        self.stdout.write(
            self.style.WARNING(
                ', '.join(
                    f'{model.__name__}: {file.name}'
                    for file, model in files_models.items()
                )
            )
        )

        for file, model in files_models.items():
            loaded = load_data(file, model, self.stdout, self.stderr)
            self.stdout.write(
                self.style.SUCCESS(
                    f'{model.__name__} :: {file.name} :: successfully '
                    f'imported {loaded} records \n'
                )
            )
