# Deploy Guide

Panduan ini memakai target yang paling umum untuk Django kecil-menengah:

- Ubuntu 22.04/24.04
- `gunicorn` sebagai WSGI server
- `systemd` untuk process manager
- `nginx` sebagai reverse proxy
- PostgreSQL untuk database production

Contoh path di server:

```text
/srv/belajaruji
```

## 1. Install package server

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx postgresql postgresql-contrib
```

## 2. Siapkan database PostgreSQL

```bash
sudo -u postgres psql
```

Di prompt PostgreSQL:

```sql
CREATE DATABASE quiz;
CREATE USER quiz_user WITH PASSWORD 'ganti-password-yang-kuat';
ALTER ROLE quiz_user SET client_encoding TO 'utf8';
ALTER ROLE quiz_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE quiz_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE quiz TO quiz_user;
\q
```

## 3. Salin kode aplikasi

```bash
sudo mkdir -p /srv/belajaruji
sudo chown $USER:$USER /srv/belajaruji
git clone <URL-REPO-ANDA> /srv/belajaruji
cd /srv/belajaruji
```

Jika deploy dari source lokal tanpa Git, salin seluruh folder project ke path tersebut.

## 4. Buat virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Siapkan environment production

```bash
cp deploy/.env.production.example .env
```

Edit `.env` lalu minimal isi:

```env
APP_ENV=production
DEBUG=False
SECRET_KEY=ganti-dengan-secret-random-yang-panjang-dan-aman
ALLOWED_HOSTS=quiz.example.com
CSRF_TRUSTED_ORIGINS=https://quiz.example.com
SITE_DOMAIN=quiz.example.com
SITE_NAME=BelajarUji
ACCOUNT_DEFAULT_HTTP_PROTOCOL=https
DATABASE_URL=postgres://quiz_user:ganti-password@127.0.0.1:5432/quiz
USE_PROXY_SSL_HEADER=True
USE_X_FORWARDED_HOST=True
USE_X_FORWARDED_PORT=True
```

Jika domain berbeda atau ada subdomain, sesuaikan `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, dan `SITE_DOMAIN`.

## 6. Jalankan step deploy aplikasi

```bash
chmod +x scripts/run_gunicorn.sh scripts/deploy_prod.sh
./scripts/deploy_prod.sh
```

Script ini akan:

- install/update dependency
- `migrate`
- `collectstatic`
- `check --deploy`

## 7. Sinkronkan Django Site

Jika memakai Google login atau domain production:

```bash
venv/bin/python manage.py sync_site
```

## 8. Buat superuser

```bash
venv/bin/python manage.py createsuperuser
```

## 9. Pasang `systemd` service

Salin template service:

```bash
sudo cp deploy/systemd/belajaruji.service.example /etc/systemd/system/belajaruji.service
```

Edit file tersebut lalu pastikan path berikut benar:

- `WorkingDirectory=/srv/belajaruji`
- `EnvironmentFile=/srv/belajaruji/.env`
- `ExecStart=/srv/belajaruji/scripts/run_gunicorn.sh`

Lalu aktifkan:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now belajaruji
sudo systemctl status belajaruji
```

Perintah penting:

```bash
sudo journalctl -u belajaruji -f
sudo systemctl restart belajaruji
```

## 10. Pasang `nginx`

Salin template config:

```bash
sudo cp deploy/nginx/belajaruji.conf.example /etc/nginx/sites-available/belajaruji
```

Edit file tersebut lalu sesuaikan:

- `server_name quiz.example.com`
- alias `/srv/belajaruji/staticfiles/`
- alias `/srv/belajaruji/media/`
- `proxy_pass http://127.0.0.1:8001`

Aktifkan site:

```bash
sudo ln -s /etc/nginx/sites-available/belajaruji /etc/nginx/sites-enabled/belajaruji
sudo nginx -t
sudo systemctl reload nginx
```

## 11. Tambahkan HTTPS

Paling praktis dengan Let's Encrypt:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d quiz.example.com
```

Setelah HTTPS aktif, verifikasi lagi:

- `.env` memakai `ACCOUNT_DEFAULT_HTTP_PROTOCOL=https`
- `CSRF_TRUSTED_ORIGINS` memakai `https://...`
- `USE_PROXY_SSL_HEADER=True`

## 12. Verifikasi akhir

```bash
curl -I http://quiz.example.com/healthz
curl -I https://quiz.example.com/healthz
venv/bin/python manage.py check --deploy
```

Cek manual juga:

- `/`
- `/admin/`
- login user biasa
- upload import soal via admin
- file static termuat normal

## Update deploy berikutnya

Setelah pull code baru:

```bash
cd /srv/belajaruji
git pull
./scripts/deploy_prod.sh
sudo systemctl restart belajaruji
```

## Troubleshooting cepat

`502 Bad Gateway`

- cek `sudo systemctl status belajaruji`
- cek `sudo journalctl -u belajaruji -f`
- pastikan `GUNICORN_PORT` sama dengan `proxy_pass`

Static file 404

- pastikan `collectstatic` sukses
- cek alias nginx menuju `/srv/belajaruji/staticfiles/`

Redirect loop HTTP/HTTPS

- cek `USE_PROXY_SSL_HEADER`
- cek nginx mengirim `X-Forwarded-Proto`
- cek TLS termination memang terjadi di nginx/proxy yang sama

Upload gambar gagal

- cek permission folder `media/`
- pastikan user service (`www-data`) bisa menulis ke folder tersebut
