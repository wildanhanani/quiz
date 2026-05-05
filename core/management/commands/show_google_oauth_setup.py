from urllib.parse import urlsplit

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Tampilkan nilai Google OAuth yang perlu diisi di Google Cloud Console.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--protocol',
            default=getattr(settings, 'ACCOUNT_DEFAULT_HTTP_PROTOCOL', 'https'),
            help='Protocol yang dipakai app, misalnya http atau https.',
        )
        parser.add_argument(
            '--domain',
            default=getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
            help='Domain site aktif, misalnya localhost:8000 atau belajaruji.com.',
        )

    def handle(self, *args, **options):
        protocol = options['protocol'].strip().lower()
        domain = options['domain'].strip().rstrip('/')

        base_origin = f'{protocol}://{domain}'
        redirect_uri = f'{base_origin}/accounts/google/login/callback/'

        origins = [base_origin]
        if domain.startswith('localhost:'):
            localhost_port = domain.split(':', 1)[1]
            origins.append(f'{protocol}://127.0.0.1:{localhost_port}')
        elif domain == 'localhost':
            origins.append(f'{protocol}://127.0.0.1')

        self.stdout.write('Google Cloud Console checklist')
        self.stdout.write('')
        self.stdout.write('Authorized JavaScript origins:')
        for origin in origins:
            self.stdout.write(f'- {origin}')

        self.stdout.write('')
        self.stdout.write('Authorized redirect URIs:')
        self.stdout.write(f'- {redirect_uri}')

        if any(origin.startswith('http://') for origin in origins):
            self.stdout.write('')
            self.stdout.write(
                'Catatan: `http` cocok untuk local development. Untuk produksi gunakan `https`.'
            )
