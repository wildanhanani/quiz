from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sinkronkan record django.contrib.sites sesuai konfigurasi environment.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--site-id',
            type=int,
            default=settings.SITE_ID,
            help='ID site yang akan disinkronkan.',
        )
        parser.add_argument(
            '--domain',
            default=getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
            help='Domain site, misalnya localhost:8000 atau belajaruji.com.',
        )
        parser.add_argument(
            '--name',
            default=getattr(settings, 'SITE_NAME', 'BelajarUji'),
            help='Nama site yang tampil di admin.',
        )

    def handle(self, *args, **options):
        site, created = Site.objects.update_or_create(
            id=options['site_id'],
            defaults={
                'domain': options['domain'],
                'name': options['name'],
            },
        )
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} site #{site.id}: {site.domain} ({site.name})'
            )
        )
