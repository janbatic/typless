import datetime

from django.core.management.base import BaseCommand

from documents.models import Documents


class Command(BaseCommand):
    def handle(self, *args, **options):
        documents = []
        day = 4
        for i in range(300):

            documents.append(
                dict(
                    number=str(i),
                    type="PDF",
                    date=datetime.date(2020, 6, day)
                )
            )
            if i % 15 == 0:
                day += 1

        Documents.put_batch(*documents)
