import csv
import os
from typing import Any, List

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import ForeignKey

from ._settings import model_by_filename


class Command(BaseCommand):
    help = 'Load data from csv files into database.'

    @staticmethod
    def is_related(model_object: Any, field_name: Any) -> bool:
        """Model field is related to foreign key."""
        field = model_object._meta.get_field(field_name)
        return field.is_relation

    @staticmethod
    def add_suffix_for_related(model: Any, keys: List[str]) -> None:
        """Add id suffix for all related fields."""
        instance = model()
        for i, field_name in enumerate(keys):
            if 'id' in field_name:
                continue
            if Command.is_related(instance, field_name):
                keys[i] += "_id"

    def handle(self, *args, **options):
        """Load data from csv files to database."""
        for filename, model in model_by_filename.items():
            filename += '.csv'
            path = os.path.join(settings.STATIC_DATA, filename)

            with open(path, encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                keys = next(reader)
                Command.add_suffix_for_related(model, keys)
                update, error = False, False
                for row in reader:
                    kwargs = {key: column for key, column in zip(keys, row)}
                    object, created = model.objects.update_or_create(**kwargs)
                    if not object:
                        error = True
                    elif not created:
                        update = True

                cout = self.stdout.write
                cerr = self.stderr.write
                if error:
                    cerr(self.style.ERROR(f'Not load {model.__name__}'))
                elif update:
                    cout(self.style.SUCCESS(f'Update {model.__name__}'))
                else:
                    cout(self.style.SUCCESS(f'Created {model.__name__}'))
