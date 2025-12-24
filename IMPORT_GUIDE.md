# 📚 Panduan Import Soal Quiz

## Cara Menggunakan Fitur Import Soal

### 1. Akses Halaman Import
1. Login ke Admin Panel: `http://127.0.0.1:8000/admin/`
2. Klik menu **"Categories"** di sidebar
3. Klik tombol **"Import Questions from CSV"** di pojok kanan atas

### 2. Format File CSV

**✨ Delimiter Support:**
File CSV bisa menggunakan **koma (,)** atau **titik koma (;)** sebagai pemisah kolom. Sistem akan **otomatis mendeteksi** delimiter yang digunakan!

**Kapan menggunakan semicolon (;)?**
- Jika pertanyaan atau pilihan jawaban mengandung koma di dalam teks
- Contoh: "Menurut UUD 1945, siapa yang berhak mengangkat menteri?"

File CSV harus memiliki kolom-kolom berikut (dengan header):

| Kolom | Deskripsi | Wajib? | Contoh | Max Length |
|-------|-----------|--------|--------|------------|
| `category` | Nama kategori quiz | ✅ Ya | "TWK" | 100 char |
| `category_description` | Deskripsi kategori | ❌ Tidak | "Tes Wawasan Kebangsaan" | - |
| `question` | Teks pertanyaan | ✅ Ya | "Pancasila terdiri dari berapa sila?" | **Unlimited** |
| `order` | Urutan soal | ✅ Ya | 1, 2, 3, ... | - |
| `choice_1` | Pilihan jawaban 1 | ✅ Ya | "3" | 500 char |
| `choice_2` | Pilihan jawaban 2 | ✅ Ya | "4" | 500 char |
| `choice_3` | Pilihan jawaban 3 | ✅ Ya | "5" | 500 char |
| `choice_4` | Pilihan jawaban 4 | ✅ Ya | "6" | 500 char |
| `choice_5` | Pilihan jawaban 5 | ❌ **OPSIONAL** | "7" | 500 char |
| `correct_answer` | Nomor jawaban benar (1-5) | ✅ Ya | 2 | - |

### 3. Contoh File CSV

#### Contoh dengan 4 pilihan jawaban (comma delimiter):
```csv
category,category_description,question,order,choice_1,choice_2,choice_3,choice_4,correct_answer
TWK,Tes Wawasan Kebangsaan,Pancasila terdiri dari berapa sila?,1,3,4,5,6,3
TIU,Tes Intelegensi Umum,Berapa hasil 5 x 5?,2,20,25,30,35,2
```

#### Contoh dengan 4 pilihan jawaban (semicolon delimiter):
```csv
category;category_description;question;order;choice_1;choice_2;choice_3;choice_4;correct_answer
TWK;Tes Wawasan Kebangsaan;Pancasila terdiri dari berapa sila?;1;3;4;5;6;3
TIU;Tes Intelegensi Umum;Berapa hasil 5 x 5?;2;20;25;30;35;2
```

#### Contoh dengan 5 pilihan jawaban (semicolon):
```csv
category;category_description;question;order;choice_1;choice_2;choice_3;choice_4;choice_5;correct_answer
TWK;Tes Wawasan Kebangsaan;Siapa presiden pertama RI?;1;Soekarno;Soeharto;Habibie;Megawati;SBY;1
TIU;Tes Intelegensi Umum;Hasil 10 + 5 adalah?;2;10;12;15;18;20;3
```

#### Contoh campuran (4 dan 5 pilihan dengan semicolon):
```csv
category;category_description;question;order;choice_1;choice_2;choice_3;choice_4;choice_5;correct_answer
TWK;Tes Wawasan Kebangsaan;Pancasila terdiri dari berapa sila?;1;3;4;5;6;;3
TWK;Tes Wawasan Kebangsaan;Siapa presiden pertama RI?;2;Soekarno;Soeharto;Habibie;Megawati;SBY;1
```

**Catatan:** Kosongkan `choice_5` jika hanya menggunakan 4 pilihan.

### 4. Upload File
1. Klik tombol **"Choose File"** atau **"Browse"**
2. Pilih file CSV Anda
3. Klik **"Upload and Import"**
4. Sistem akan otomatis:
   - Membuat kategori baru jika belum ada
   - Menambahkan semua soal dan pilihan jawaban (4 atau 5 pilihan)
   - Menampilkan pesan sukses dengan jumlah soal yang berhasil diimport

### 5. Tips & Catatan

✅ **DO:**
- Pastikan file dalam format CSV (bukan Excel .xlsx)
- Gunakan encoding UTF-8
- Isi semua kolom yang wajib
- Gunakan nomor 1-5 untuk `correct_answer`
- **choice_5 boleh dikosongkan** jika hanya butuh 4 pilihan
- **Gunakan semicolon (;)** jika data mengandung koma

❌ **DON'T:**
- Jangan kosongkan kolom `category`, `question`, atau `order`
- Jangan gunakan karakter khusus yang aneh di nama file
- Jangan upload file yang terlalu besar (max 1000 soal per upload)
- Jangan campur delimiter (pilih comma ATAU semicolon, jangan keduanya)

### 6. Troubleshooting

**Error: "File must be a CSV"**
- Pastikan file berekstensi `.csv`, bukan `.xlsx` atau `.txt`

**Error: "value too long for type character varying"**
- ✅ **SUDAH DIPERBAIKI!** Question text sekarang unlimited
- Pastikan setiap pilihan jawaban (choice) tidak lebih dari 500 karakter
- Jika ada pilihan yang terlalu panjang, singkat atau pecah menjadi beberapa soal

**Error: "Error importing CSV"**
- Periksa format CSV Anda
- Pastikan semua kolom header sesuai
- Cek apakah ada baris kosong di tengah file
- Pastikan encoding UTF-8

**Soal tidak muncul**
- Refresh halaman admin
- Periksa apakah kategori sudah dibuat
- Cek di menu "Questions" untuk melihat soal yang sudah diimport

---

## Contoh Workflow

1. Buat file Excel dengan soal-soal Anda
2. Tambahkan kolom `choice_5` jika ada soal dengan 5 pilihan
3. Save As → **CSV (Comma delimited) (*.csv)**
4. Upload ke Admin Panel
5. Verifikasi soal sudah masuk di menu "Questions"
6. Test quiz di halaman user

## Template CSV

Lihat file `sample_questions.csv` di root project untuk template lengkap dengan contoh 4 dan 5 pilihan jawaban.

Selamat menggunakan! 🚀
