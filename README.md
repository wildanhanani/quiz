# 🎓 Test Soal CPNS & BUMN - Complete Guide

## ✅ Update Terbaru: Support 5 Pilihan Jawaban!

CSV Import sekarang mendukung **4 atau 5 pilihan jawaban** per soal.

---

## 📋 Ringkasan Fitur

### 🎨 Design & Branding
- ✅ **Light Theme** - Background putih, clean & professional
- ✅ **Branding**: Test Soal CPNS & BUMN
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

# 2. Run server
python manage.py runserver

# 3. Akses
# - Website: http://127.0.0.1:8000/
# - Admin: http://127.0.0.1:8000/admin/
```

### Default Login
- **Admin**: `admin` / `admin`
- **User**: `testuser` / `test123`

---

## 📝 CSV Import dengan 5 Pilihan Jawaban

### Format CSV

**Header Wajib:**
```csv
category,category_description,question,order,choice_1,choice_2,choice_3,choice_4,choice_5,correct_answer
```

### Contoh 1: Soal dengan 4 Pilihan
```csv
TWK,Tes Wawasan Kebangsaan,Pancasila terdiri dari berapa sila?,1,3,4,5,6,,3
```
**Catatan:** `choice_5` dikosongkan

### Contoh 2: Soal dengan 5 Pilihan
```csv
TWK,Tes Wawasan Kebangsaan,Siapa presiden pertama RI?,1,Soekarno,Soeharto,Habibie,Megawati,SBY,1
```

### Contoh 3: File Lengkap (Campuran)
```csv
category,category_description,question,order,choice_1,choice_2,choice_3,choice_4,choice_5,correct_answer
TWK,Tes Wawasan Kebangsaan,Pancasila terdiri dari berapa sila?,1,3,4,5,6,,3
TWK,Tes Wawasan Kebangsaan,Siapa presiden pertama RI?,2,Soekarno,Soeharto,Habibie,Megawati,SBY,1
TIU,Tes Intelegensi Umum,Berapa hasil 5 x 5?,3,20,25,30,35,,2
TKP,Tes Karakteristik Pribadi,Jika menemukan uang?,4,Ambil,Lapor polisi,Biarkan,Beri orang lain,Simpan dulu,2
```

### Cara Import
1. Login ke `/admin/`
2. Klik **Categories** → **Import Questions from CSV**
3. Upload file CSV
4. Sistem otomatis detect 4 atau 5 pilihan
5. Done! ✅

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
