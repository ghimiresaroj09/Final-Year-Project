import csv
from django.core.management.base import BaseCommand
from product.models import KnowledgeBase


class Command(BaseCommand):
    help = 'Import KnowledgeBase entries from a CSV file. Columns: title,content,keywords,is_active'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to CSV file to import')

    def handle(self, *args, **options):
        path = options['file']
        created = 0
        updated = 0
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader, start=1):
                    title = (row.get('title') or '').strip()
                    content = (row.get('content') or '').strip()
                    keywords = (row.get('keywords') or '').strip()
                    is_active_raw = (row.get('is_active') or '1').strip()
                    is_active = str(is_active_raw).lower() in ('1', 'true', 'yes', 'y')

                    if not title or not content:
                        self.stdout.write(self.style.WARNING(f"Skipping row {i}: missing title or content"))
                        continue

                    obj, created_flag = KnowledgeBase.objects.update_or_create(
                        title=title,
                        defaults={
                            'content': content,
                            'keywords': keywords,
                            'is_active': is_active,
                        }
                    )
                    if created_flag:
                        created += 1
                    else:
                        updated += 1

            self.stdout.write(self.style.SUCCESS(f'Import finished: created={created}, updated={updated}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing KB: {e}'))
