# 🎓 BelajarUji CPNS & BUMN - Complete Guide

## ✅ Update Terbaru: Support 5 Pilihan Jawaban!

CSV Import sekarang mendukung **4 atau 5 pilihan jawaban** per soal.

---

## 📋 Ringkasan Fitur

### 🎨 Design & Branding
- ✅ **Light Theme** - Background putih, clean & professional
- ✅ **Branding**: BelajarUji CPNS & BUMN
- ✅ **Color**: Blue (#2563eb) - Formal & trustworthy

### 💰 Paket Berlangganan
| Paket | Harga | Kategori | Attempt | Pembahasan |
|-------|-------|----------|---------|------------|
| **Gratis** | Rp 0 | Gratis saja | **1x** | ✅ |
| **Basic** | Rp 10.000 | 5 kategori | **3x** | ✅ |
| **Premium** | Rp 50.000 | Semua | **5x** | ✅ + Tips |

### 🆕 Fitur Utama
1. ✅ **Subscription System** dengan attempt limit
2. ✅ **Pembahasan Jawaban** lengkap setelah quiz
3. ✅ **Premium Categories** untuk paket berbayar
4. ✅ **CSV Import** dengan support **4 atau 5 pilihan jawaban**
5. ✅ **Progress Tracking** & riwayat lengkap
6. ✅ **Admin Approval** untuk user baru

---

## 🚀 Quick Start

```bash
# 1. Setup (otomatis)
chmod +x setup.sh
./setup.sh

# 2. Start dev server
chmod +x run_dev.sh
./run_dev.sh

# 3. Akses
# - Website: http://127.0.0.1:8000/ (atau port berikutnya jika 8000 bentrok)
# - Admin: http://127.0.0.1:8000/admin/
# - Health Check: http://127.0.0.1:8000/healthz/
```

Jika `DATABASE_URL` tidak diisi dan variabel `DB_*` tidak tersedia, aplikasi akan fallback ke SQLite lokal (`db.sqlite3`) untuk development.

### Environment

- Gunakan `.env.example` sebagai template konfigurasi lokal.
- `APP_ENV=development` untuk lokal, dan `APP_ENV=production` untuk deploy nyata.
- Default setup sekarang mengarah ke mode SQLite agar project bisa langsung jalan tanpa PostgreSQL.
- Jika ingin memakai PostgreSQL, isi `DATABASE_URL` atau `DB_*` di `.env` sebelum menjalankan `./run_dev.sh`.
- `run_dev.sh` akan otomatis mencari port kosong mulai dari `8000`.
- Untuk Google login, isi juga `SITE_ID`, `SITE_DOMAIN`, `SITE_NAME`, dan `ACCOUNT_DEFAULT_HTTP_PROTOCOL`.
- Saat `APP_ENV=production`, aplikasi otomatis mengaktifkan hardening HTTPS/cookie/HSTS/logging dasar. Pastikan `SECRET_KEY`, `ALLOWED_HOSTS`, dan `CSRF_TRUSTED_ORIGINS` diisi dengan benar.
- Styling sekarang dibuild ke asset lokal di `static/css/app.css`, tidak lagi mengandalkan Tailwind CDN saat runtime.

### Frontend CSS

```bash
npm install
npm run build:css
```

Untuk development saat mengubah template/class Tailwind:

```bash
npm run watch:css
```

### Default Login
- **Admin**: `admin` / `admin`
- **User**: `testuser` / `test123`

### Google Login

1. Isi environment:
   - `SITE_ID=1`
   - `SITE_DOMAIN=localhost:8000`
   - `SITE_NAME=BelajarUji`
   - `ACCOUNT_DEFAULT_HTTP_PROTOCOL=http`
2. Sinkronkan record site:
   - `venv/bin/python manage.py sync_site`
3. Lihat nilai OAuth yang perlu diisi ke Google Cloud Console:
   - `venv/bin/python manage.py show_google_oauth_setup`
4. Di admin, buat `Social application` baru:
   - Provider: `Google`
   - Isi `Client id` dan `Secret key`
   - Hubungkan ke site aktif yang domain-nya sama dengan `SITE_DOMAIN`

Tombol Google di halaman login/register hanya tampil jika `SocialApp` Google untuk `SITE_ID` aktif memang ada.

### Production Baseline

Minimum yang sebaiknya diisi saat deploy:

```env
APP_ENV=production
DEBUG=False
SECRET_KEY=ganti-dengan-secret-yang-panjang-dan-random
ALLOWED_HOSTS=quiz.example.com
CSRF_TRUSTED_ORIGINS=https://quiz.example.com
SITE_DOMAIN=quiz.example.com
SITE_NAME=BelajarUji
ACCOUNT_DEFAULT_HTTP_PROTOCOL=https
USE_PROXY_SSL_HEADER=True
USE_X_FORWARDED_HOST=True
USE_X_FORWARDED_PORT=True
DATABASE_URL=postgres://user:password@db-host:5432/quiz
```

Catatan deploy:
- Jalankan `venv/bin/python manage.py migrate`
- Jalankan `venv/bin/python manage.py collectstatic --noinput`
- Jalankan `venv/bin/python manage.py check --deploy`
- `healthz` sengaja dikecualikan dari HTTPS redirect default agar lebih mudah dipakai untuk probe internal
- Jika TLS termination tidak memakai reverse proxy yang mengirim header forwarded, ubah `USE_PROXY_SSL_HEADER=False`
- Panduan deploy lengkap ada di `DEPLOY.md`

---

## 📝 Panduan Import Soal (CSV & Gambar)

### Opsi 1: CSV / Excel (Teks Saja)
Gunakan file `.csv` atau `.xlsx` jika soal hanya berupa teks.

### Opsi 2: ZIP File (Soal Bergambar) 📸
Jika soal memiliki gambar, Anda harus mengupload file **.zip** yang berisi:
1. File `.csv` (daftar soal)
2. File gambar `.jpg` atau `.png`

**Struktur ZIP:**
```
soal_cpns.zip
├── soal.csv
├── gambar1.jpg
├── rumus_mtk.png
└── garuda.jpg
```

---

### Format CSV
Tambahkan kolom `image` di file CSV Anda.

**Header Wajib:**
```csv
category;question;image;choice_1;choice_2;choice_3;choice_4;choice_5;correct_answer
```
*(Gunakan titik koma `;` jika teks soal mengandung koma)*

### Contoh Isi CSV:

**1. Soal Bergambar 4 Pilihan:**
```csv
TWK;Lambang negara di samping adalah?;garuda.jpg;Bintang;Pohon Beringin;Garuda;Padi Kapas;;3
```
*(Pastikan file `garuda.jpg` ada di dalam ZIP)*

**2. Soal Teks Biasa 5 Pilihan:**
```csv
TIU;Siapa penemu lampu?;(kosongkan);Tesla;Edison;Einstein;Grahambell;Newton;2
```

Template tambahan:
- `sample_questions.csv` / `sample_questions_semicolon.csv` untuk contoh umum
- `sample_questions_cpns.csv` / `sample_questions_cpns_semicolon.csv` untuk contoh TWK/TIU/TKP yang lebih realistis

---

### Cara Import
1. Login ke `/admin/`
2. Klik **Categories** → **Import Questions from CSV**
3. Pilih File:
   - Upload **.csv** atau **.xlsx** (jika teks saja)
   - Upload **.zip** (jika ada gambar + file csv/xlsx)
4. Klik **Upload and Import**
5. Sistem otomatis mengekstrak & mencocokkan gambar. ✅

---

## 👥 Panduan User

### 1. Registrasi & Login
```
1. Klik "Daftar" → Isi form
2. Status: Pending (tunggu admin approve)
3. Admin approve di /admin/ → Users → Centang "Active"
4. Login dengan kredensial Anda
```

### 2. Mengerjakan Quiz
```
1. Dashboard → Pilih kategori
2. Kerjakan soal (4 atau 5 pilihan)
3. Submit jawaban
4. Lihat pembahasan:
   - ✅ Jawaban benar (hijau)
   - ❌ Jawaban salah (merah)
   - Skor & persentase
```

### 3. Upgrade Paket
```
Hubungi admin untuk upgrade ke Basic/Premium
Admin akan update di: Admin Panel → Subscriptions
```

---

## 🔧 Panduan Admin

### 1. Approve User
```
Admin Panel → Users → Pilih user → Centang "Active" → Save
```

### 2. Upgrade Paket User
**Via Admin Panel:**
```
Subscriptions → Pilih user → Edit:
- Package: BASIC atau PREMIUM
- Max attempts: 3 (Basic) atau 5 (Premium)
- Max categories: 5 (Basic) atau 999 (Premium)
→ Save
```

**Via Script:**
```bash
python manage.py shell < update_subscription.py
# Ikuti prompt interaktif
```

### 3. Tambah Kategori
```
Categories → Add Category:
- Name: Nama kategori
- Description: Deskripsi
- Is premium: ✅ (jika kategori premium)
→ Save
```

### 4. Import Soal CSV
```
Categories → "Import Questions from CSV"
Upload file dengan format:
- 4 pilihan: kosongkan choice_5
- 5 pilihan: isi semua choice_1 sampai choice_5
```

### 5. Dashboard Admin
Beranda `/admin/` sekarang menampilkan statistik ringkas:
- total user aktif/pending
- total attempt dan attempt hari ini
- total kategori, soal, dan opsi jawaban
- rata-rata akurasi
- kategori paling sering dikerjakan
- attempt terbaru

---

## 📊 Database Models

### Subscription
```python
- user (OneToOne)
- package (FREE/BASIC/PREMIUM)
- max_attempts_per_quiz (999/3/5)
- max_categories (999/5/999)
```

### Category
```python
- name, description
- is_premium (boolean)
```

### Question & Choice
```python
Question:
  - category, text, order

Choice:
  - question, text, is_correct
  # Bisa 4 atau 5 choices per question
```

### QuizAttempt
```python
- user, category, score, total_questions
- answers (JSONField) - untuk review
- completed_at
```

---

## 🎯 Testing Flow

### Test CSV Import dengan 5 Pilihan
```bash
# 1. Login admin
http://127.0.0.1:8000/admin/

# 2. Import sample_questions.csv
Categories → Import Questions from CSV → Upload

# 3. Verify
Questions → Lihat soal yang diimport
- TWK: 2 soal (1 dengan 4, 1 dengan 5 pilihan)
- TIU: 2 soal (1 dengan 4, 1 dengan 5 pilihan)
- TKP: 1 soal (5 pilihan)

# 4. Test di user side
Login sebagai testuser → Kerjakan quiz → Lihat pembahasan
```

---

## 📁 File Structure

```
quiz/
├── quiz/
│   ├── models.py          # Subscription, Category, Question, Choice
│   ├── views.py           # Dashboard, quiz logic, result
│   ├── admin.py           # CSV import (support 4-5 choices)
│   └── urls.py
├── templates/
│   ├── base.html          # Light theme
│   ├── index.html         # Landing page
│   ├── pricing.html       # Paket berlangganan
│   ├── quiz/
│   │   ├── dashboard.html
│   │   ├── take_quiz.html
│   │   └── result.html    # Pembahasan jawaban
│   └── admin/
│       └── import_questions.html  # CSV import UI
├── sample_questions.csv   # Template (4 & 5 pilihan)
├── update_subscription.py # Script upgrade paket
├── IMPORT_GUIDE.md       # Panduan CSV import
└── README.md             # This file
```

---

## 🆕 Changelog

### v2.0 (Latest)
- ✅ **Support 5 pilihan jawaban** di CSV import
- ✅ Light theme (background putih)
- ✅ Subscription system (FREE/BASIC/PREMIUM)
- ✅ Pembahasan jawaban lengkap
- ✅ Attempt limit per paket
- ✅ Premium categories

### v1.0
- ✅ Basic quiz system
- ✅ Admin panel
- ✅ CSV import (4 pilihan)

---

## 💡 Tips & Best Practices

### Untuk Admin
1. Set kategori premium untuk konten eksklusif
2. Monitor attempt count per user
3. Gunakan CSV import untuk bulk upload
4. Backup database secara berkala

### Untuk User
1. Pelajari pembahasan setelah quiz
2. Ulangi quiz untuk meningkatkan skor
3. Upgrade ke Premium untuk akses penuh
4. Track progress di dashboard

---

## 🐛 Troubleshooting

### CSV Import Error
**Problem:** "Error importing CSV"
**Solution:**
- Pastikan encoding UTF-8
- Cek format header
- Kosongkan choice_5 jika hanya 4 pilihan
- Lihat `sample_questions.csv` untuk referensi

### Attempt Limit
**Problem:** "Sudah mencapai batas maksimal"
**Solution:**
- Admin reset attempt: Hapus QuizAttempt untuk user tersebut
- Atau upgrade paket user

### Pembahasan Tidak Muncul
**Problem:** Halaman result kosong
**Solution:**
- Pastikan `answers` field terisi di QuizAttempt
- Check browser console untuk error
- Refresh halaman

---

## 📞 Support

Untuk bantuan lebih lanjut:
- 📧 Email: admin@testsoal.com
- 📱 WhatsApp: 08xx-xxxx-xxxx
- 📚 Docs: `IMPORT_GUIDE.md`

---

**Built with ❤️ using Django & Tailwind CSS**

Last Updated: 23 Desember 2024
