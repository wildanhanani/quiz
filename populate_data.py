"""
Script to populate the database with dummy data for testing
Run with: python manage.py shell < populate_data.py
"""

from django.contrib.auth.models import User
from quiz.models import Category, Question, Choice

# Create test user (active)
print("Creating test user...")
if not User.objects.filter(username='testuser').exists():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='test123',
        is_active=True
    )
    print(f"✓ Created user: testuser (password: test123)")
else:
    print("✓ User 'testuser' already exists")

# Create Categories
print("\nCreating quiz categories...")
categories_data = [
    {
        'name': 'Pengetahuan Umum',
        'description': 'Tes wawasan umum tentang berbagai topik'
    },
    {
        'name': 'Teknologi & Programming',
        'description': 'Kuis seputar dunia teknologi dan pemrograman'
    },
    {
        'name': 'Logika & Numerik',
        'description': 'Latihan logika dasar, pola angka, dan hitungan cepat'
    },
    {
        'name': 'Bahasa Indonesia',
        'description': 'Soal ejaan, sinonim, antonim, dan pemahaman kata'
    },
    {
        'name': 'TWK CPNS',
        'description': 'Latihan wawasan kebangsaan untuk persiapan seleksi CPNS'
    },
    {
        'name': 'TIU CPNS',
        'description': 'Latihan intelegensi umum untuk persiapan seleksi CPNS'
    },
    {
        'name': 'TKP CPNS',
        'description': 'Latihan karakteristik pribadi untuk persiapan seleksi CPNS'
    },
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"✓ Created category: {category.name}")
    else:
        print(f"✓ Category '{category.name}' already exists")

# Create Questions for "Pengetahuan Umum"
print("\nCreating questions for 'Pengetahuan Umum'...")
pengetahuan_umum = Category.objects.get(name='Pengetahuan Umum')

questions_pu = [
    {
        'text': 'Apa ibukota Indonesia?',
        'choices': [
            {'text': 'Bandung', 'is_correct': False},
            {'text': 'Jakarta', 'is_correct': True},
            {'text': 'Surabaya', 'is_correct': False},
            {'text': 'Medan', 'is_correct': False},
        ]
    },
    {
        'text': 'Siapa presiden pertama Indonesia?',
        'choices': [
            {'text': 'Soekarno', 'is_correct': True},
            {'text': 'Soeharto', 'is_correct': False},
            {'text': 'Habibie', 'is_correct': False},
            {'text': 'Megawati', 'is_correct': False},
        ]
    },
    {
        'text': 'Berapa jumlah provinsi di Indonesia saat ini?',
        'choices': [
            {'text': '32', 'is_correct': False},
            {'text': '33', 'is_correct': False},
            {'text': '34', 'is_correct': False},
            {'text': '38', 'is_correct': True},
        ]
    },
    {
        'text': 'Apa mata uang resmi Indonesia?',
        'choices': [
            {'text': 'Ringgit', 'is_correct': False},
            {'text': 'Rupiah', 'is_correct': True},
            {'text': 'Baht', 'is_correct': False},
            {'text': 'Peso', 'is_correct': False},
        ]
    },
    {
        'text': 'Gunung tertinggi di Indonesia adalah?',
        'choices': [
            {'text': 'Gunung Semeru', 'is_correct': False},
            {'text': 'Gunung Rinjani', 'is_correct': False},
            {'text': 'Puncak Jaya', 'is_correct': True},
            {'text': 'Gunung Kerinci', 'is_correct': False},
        ]
    },
    {
        'text': 'Bhinneka Tunggal Ika memiliki arti?',
        'choices': [
            {'text': 'Bersatu kita teguh', 'is_correct': False},
            {'text': 'Berbeda-beda tetapi tetap satu', 'is_correct': True},
            {'text': 'Rakyat adalah sumber kekuasaan', 'is_correct': False},
            {'text': 'Sekali merdeka tetap merdeka', 'is_correct': False},
        ]
    },
    {
        'text': 'Lembaga yang berwenang menguji undang-undang terhadap UUD 1945 adalah?',
        'choices': [
            {'text': 'Mahkamah Agung', 'is_correct': False},
            {'text': 'Mahkamah Konstitusi', 'is_correct': True},
            {'text': 'DPR', 'is_correct': False},
            {'text': 'MPR', 'is_correct': False},
        ]
    },
    {
        'text': 'ASEAN didirikan pada tahun?',
        'choices': [
            {'text': '1965', 'is_correct': False},
            {'text': '1967', 'is_correct': True},
            {'text': '1970', 'is_correct': False},
            {'text': '1975', 'is_correct': False},
        ]
    },
    {
        'text': 'Planet terbesar dalam tata surya adalah?',
        'choices': [
            {'text': 'Bumi', 'is_correct': False},
            {'text': 'Saturnus', 'is_correct': False},
            {'text': 'Jupiter', 'is_correct': True},
            {'text': 'Mars', 'is_correct': False},
        ]
    },
    {
        'text': 'Tanggal Proklamasi Kemerdekaan Indonesia adalah?',
        'choices': [
            {'text': '17 Agustus 1945', 'is_correct': True},
            {'text': '18 Agustus 1945', 'is_correct': False},
            {'text': '1 Juni 1945', 'is_correct': False},
            {'text': '28 Oktober 1928', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_pu, 1):
    question, created = Question.objects.get_or_create(
        category=pengetahuan_umum,
        text=q_data['text'],
        defaults={'order': idx}
    )
    
    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "Teknologi & Programming"
print("\nCreating questions for 'Teknologi & Programming'...")
teknologi = Category.objects.get(name='Teknologi & Programming')

questions_tech = [
    {
        'text': 'Apa kepanjangan dari HTML?',
        'choices': [
            {'text': 'Hyper Text Markup Language', 'is_correct': True},
            {'text': 'High Tech Modern Language', 'is_correct': False},
            {'text': 'Home Tool Markup Language', 'is_correct': False},
            {'text': 'Hyperlinks and Text Markup Language', 'is_correct': False},
        ]
    },
    {
        'text': 'Bahasa pemrograman apa yang digunakan untuk membuat website dinamis?',
        'choices': [
            {'text': 'HTML', 'is_correct': False},
            {'text': 'CSS', 'is_correct': False},
            {'text': 'JavaScript', 'is_correct': True},
            {'text': 'XML', 'is_correct': False},
        ]
    },
    {
        'text': 'Apa itu Git?',
        'choices': [
            {'text': 'Bahasa pemrograman', 'is_correct': False},
            {'text': 'Version control system', 'is_correct': True},
            {'text': 'Database', 'is_correct': False},
            {'text': 'Web framework', 'is_correct': False},
        ]
    },
    {
        'text': 'Framework Python yang populer untuk web development adalah?',
        'choices': [
            {'text': 'React', 'is_correct': False},
            {'text': 'Angular', 'is_correct': False},
            {'text': 'Django', 'is_correct': True},
            {'text': 'Laravel', 'is_correct': False},
        ]
    },
    {
        'text': 'Apa fungsi utama CSS?',
        'choices': [
            {'text': 'Membuat struktur halaman web', 'is_correct': False},
            {'text': 'Styling dan tampilan halaman web', 'is_correct': True},
            {'text': 'Mengelola database', 'is_correct': False},
            {'text': 'Membuat logika pemrograman', 'is_correct': False},
        ]
    },
    {
        'text': 'Perintah Git untuk mengirim commit ke remote repository adalah?',
        'choices': [
            {'text': 'git status', 'is_correct': False},
            {'text': 'git clone', 'is_correct': False},
            {'text': 'git push', 'is_correct': True},
            {'text': 'git merge', 'is_correct': False},
        ]
    },
    {
        'text': 'Database relasional yang populer digunakan bersama Django adalah?',
        'choices': [
            {'text': 'PostgreSQL', 'is_correct': True},
            {'text': 'Redis', 'is_correct': False},
            {'text': 'ElasticSearch', 'is_correct': False},
            {'text': 'RabbitMQ', 'is_correct': False},
        ]
    },
    {
        'text': 'Apa fungsi utama framework backend?',
        'choices': [
            {'text': 'Mengatur styling halaman', 'is_correct': False},
            {'text': 'Mengelola logika server dan request', 'is_correct': True},
            {'text': 'Mengedit gambar', 'is_correct': False},
            {'text': 'Membuat animasi CSS', 'is_correct': False},
        ]
    },
    {
        'text': 'Ekstensi file Python adalah?',
        'choices': [
            {'text': '.java', 'is_correct': False},
            {'text': '.py', 'is_correct': True},
            {'text': '.js', 'is_correct': False},
            {'text': '.php', 'is_correct': False},
        ]
    },
    {
        'text': 'HTTP status code untuk halaman tidak ditemukan adalah?',
        'choices': [
            {'text': '200', 'is_correct': False},
            {'text': '301', 'is_correct': False},
            {'text': '404', 'is_correct': True},
            {'text': '500', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_tech, 1):
    question, created = Question.objects.get_or_create(
        category=teknologi,
        text=q_data['text'],
        defaults={'order': idx}
    )
    
    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "Logika & Numerik"
print("\nCreating questions for 'Logika & Numerik'...")
logika = Category.objects.get(name='Logika & Numerik')

questions_logic = [
    {
        'text': 'Jika 2, 4, 8, 16, maka angka berikutnya adalah?',
        'choices': [
            {'text': '18', 'is_correct': False},
            {'text': '24', 'is_correct': False},
            {'text': '32', 'is_correct': True},
            {'text': '36', 'is_correct': False},
        ]
    },
    {
        'text': 'Hasil dari 12 x 8 adalah?',
        'choices': [
            {'text': '86', 'is_correct': False},
            {'text': '94', 'is_correct': False},
            {'text': '96', 'is_correct': True},
            {'text': '108', 'is_correct': False},
        ]
    },
    {
        'text': 'Semua dokter adalah sarjana. Sebagian sarjana adalah dosen. Kesimpulan yang pasti benar adalah?',
        'choices': [
            {'text': 'Semua dosen adalah dokter', 'is_correct': False},
            {'text': 'Sebagian dokter adalah dosen', 'is_correct': False},
            {'text': 'Semua dokter adalah sarjana', 'is_correct': True},
            {'text': 'Sebagian sarjana bukan dokter', 'is_correct': False},
        ]
    },
    {
        'text': 'Jika harga 3 buku Rp45.000, maka harga 5 buku adalah?',
        'choices': [
            {'text': 'Rp60.000', 'is_correct': False},
            {'text': 'Rp70.000', 'is_correct': False},
            {'text': 'Rp75.000', 'is_correct': True},
            {'text': 'Rp80.000', 'is_correct': False},
        ]
    },
    {
        'text': 'Deret huruf A, C, F, J, O, ... huruf berikutnya adalah?',
        'choices': [
            {'text': 'T', 'is_correct': False},
            {'text': 'U', 'is_correct': True},
            {'text': 'V', 'is_correct': False},
            {'text': 'W', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_logic, 1):
    question, created = Question.objects.get_or_create(
        category=logika,
        text=q_data['text'],
        defaults={'order': idx}
    )

    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "Bahasa Indonesia"
print("\nCreating questions for 'Bahasa Indonesia'...")
bahasa = Category.objects.get(name='Bahasa Indonesia')

questions_bahasa = [
    {
        'text': 'Bentuk kata baku yang benar adalah?',
        'choices': [
            {'text': 'Aktifitas', 'is_correct': False},
            {'text': 'Aktivitas', 'is_correct': True},
            {'text': 'Aktipitas', 'is_correct': False},
            {'text': 'Aktifitasi', 'is_correct': False},
        ]
    },
    {
        'text': 'Sinonim kata "cermat" adalah?',
        'choices': [
            {'text': 'Ceroboh', 'is_correct': False},
            {'text': 'Teliti', 'is_correct': True},
            {'text': 'Lambat', 'is_correct': False},
            {'text': 'Bimbang', 'is_correct': False},
        ]
    },
    {
        'text': 'Antonim kata "optimis" adalah?',
        'choices': [
            {'text': 'Semangat', 'is_correct': False},
            {'text': 'Pesimis', 'is_correct': True},
            {'text': 'Antusias', 'is_correct': False},
            {'text': 'Kreatif', 'is_correct': False},
        ]
    },
    {
        'text': 'Penulisan yang tepat adalah?',
        'choices': [
            {'text': 'di rumah', 'is_correct': True},
            {'text': 'dirumah', 'is_correct': False},
            {'text': 'ke pada', 'is_correct': False},
            {'text': 'antar kota', 'is_correct': False},
        ]
    },
    {
        'text': 'Kalimat efektif yang benar adalah?',
        'choices': [
            {'text': 'Para siswa-siswa sedang belajar.', 'is_correct': False},
            {'text': 'Siswa-siswa sedang belajar semua.', 'is_correct': False},
            {'text': 'Para siswa sedang belajar.', 'is_correct': True},
            {'text': 'Para siswa sedang belajar-belajar.', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_bahasa, 1):
    question, created = Question.objects.get_or_create(
        category=bahasa,
        text=q_data['text'],
        defaults={'order': idx}
    )

    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "TWK CPNS"
print("\nCreating questions for 'TWK CPNS'...")
twk_cpns = Category.objects.get(name='TWK CPNS')

questions_twk_cpns = [
    {
        'text': 'Pancasila sebagai dasar negara ditetapkan pada tanggal?',
        'choices': [
            {'text': '1 Juni 1945', 'is_correct': False},
            {'text': '17 Agustus 1945', 'is_correct': False},
            {'text': '18 Agustus 1945', 'is_correct': True},
            {'text': '22 Juni 1945', 'is_correct': False},
        ]
    },
    {
        'text': 'Lembaga yang berwenang mengubah dan menetapkan UUD 1945 adalah?',
        'choices': [
            {'text': 'DPR', 'is_correct': False},
            {'text': 'MPR', 'is_correct': True},
            {'text': 'Presiden', 'is_correct': False},
            {'text': 'Mahkamah Konstitusi', 'is_correct': False},
        ]
    },
    {
        'text': 'Semboyan Bhinneka Tunggal Ika menekankan pentingnya?',
        'choices': [
            {'text': 'Persaingan antar daerah', 'is_correct': False},
            {'text': 'Persatuan dalam keberagaman', 'is_correct': True},
            {'text': 'Kesamaan budaya secara mutlak', 'is_correct': False},
            {'text': 'Otonomi tanpa batas', 'is_correct': False},
        ]
    },
    {
        'text': 'Contoh sikap bela negara di lingkungan kerja adalah?',
        'choices': [
            {'text': 'Menyebarkan informasi rahasia kantor', 'is_correct': False},
            {'text': 'Menjaga integritas dan menaati aturan', 'is_correct': True},
            {'text': 'Mengutamakan kelompok sendiri', 'is_correct': False},
            {'text': 'Mengabaikan pelayanan publik', 'is_correct': False},
        ]
    },
    {
        'text': 'Hubungan yang benar antara pusat dan daerah dalam NKRI adalah?',
        'choices': [
            {'text': 'Daerah sepenuhnya terpisah dari pusat', 'is_correct': False},
            {'text': 'Pusat dan daerah bekerja sesuai pembagian kewenangan', 'is_correct': True},
            {'text': 'Daerah dapat membatalkan UUD', 'is_correct': False},
            {'text': 'Pusat tidak boleh mengawasi daerah', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_twk_cpns, 1):
    question, created = Question.objects.get_or_create(
        category=twk_cpns,
        text=q_data['text'],
        defaults={'order': idx}
    )

    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "TIU CPNS"
print("\nCreating questions for 'TIU CPNS'...")
tiu_cpns = Category.objects.get(name='TIU CPNS')

questions_tiu_cpns = [
    {
        'text': 'Jika 3, 6, 12, 24, maka angka berikutnya adalah?',
        'choices': [
            {'text': '36', 'is_correct': False},
            {'text': '42', 'is_correct': False},
            {'text': '48', 'is_correct': True},
            {'text': '54', 'is_correct': False},
        ]
    },
    {
        'text': 'Hasil dari 125 dibagi 5 adalah?',
        'choices': [
            {'text': '15', 'is_correct': False},
            {'text': '20', 'is_correct': False},
            {'text': '25', 'is_correct': True},
            {'text': '30', 'is_correct': False},
        ]
    },
    {
        'text': 'Semua auditor teliti. Sebagian pegawai adalah auditor. Kesimpulan yang pasti benar adalah?',
        'choices': [
            {'text': 'Semua pegawai teliti', 'is_correct': False},
            {'text': 'Sebagian pegawai teliti', 'is_correct': True},
            {'text': 'Semua auditor pegawai', 'is_correct': False},
            {'text': 'Sebagian auditor tidak teliti', 'is_correct': False},
        ]
    },
    {
        'text': 'Jika harga 4 map Rp28.000, maka harga 7 map adalah?',
        'choices': [
            {'text': 'Rp42.000', 'is_correct': False},
            {'text': 'Rp49.000', 'is_correct': True},
            {'text': 'Rp56.000', 'is_correct': False},
            {'text': 'Rp63.000', 'is_correct': False},
        ]
    },
    {
        'text': 'Antonim kata "efisien" adalah?',
        'choices': [
            {'text': 'Tepat', 'is_correct': False},
            {'text': 'Gesit', 'is_correct': False},
            {'text': 'Boros', 'is_correct': True},
            {'text': 'Hemat', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_tiu_cpns, 1):
    question, created = Question.objects.get_or_create(
        category=tiu_cpns,
        text=q_data['text'],
        defaults={'order': idx}
    )

    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

# Create Questions for "TKP CPNS"
print("\nCreating questions for 'TKP CPNS'...")
tkp_cpns = Category.objects.get(name='TKP CPNS')

questions_tkp_cpns = [
    {
        'text': 'Atasan memberi target mendadak saat pekerjaan Anda penuh. Sikap terbaik adalah?',
        'choices': [
            {'text': 'Menolak tanpa solusi', 'is_correct': False},
            {'text': 'Menyusun prioritas dan mengomunikasikan kapasitas', 'is_correct': True},
            {'text': 'Mengerjakan seadanya', 'is_correct': False},
            {'text': 'Menyalahkan rekan kerja', 'is_correct': False},
        ]
    },
    {
        'text': 'Rekan tim melakukan kesalahan input data pelayanan. Anda akan?',
        'choices': [
            {'text': 'Mengoreksi diam-diam lalu membiarkannya', 'is_correct': False},
            {'text': 'Memberi tahu dan membantu memperbaiki proses', 'is_correct': True},
            {'text': 'Menunggu diminta atasan', 'is_correct': False},
            {'text': 'Menjadikannya bahan keluhan grup', 'is_correct': False},
        ]
    },
    {
        'text': 'Masyarakat marah karena antrean panjang. Tindakan paling tepat adalah?',
        'choices': [
            {'text': 'Meminta mereka diam', 'is_correct': False},
            {'text': 'Menjelaskan situasi dengan tenang dan memberi solusi', 'is_correct': True},
            {'text': 'Mengabaikan keluhan', 'is_correct': False},
            {'text': 'Meminta satpam langsung mengusir', 'is_correct': False},
        ]
    },
    {
        'text': 'Anda diminta membantu unit lain di luar tugas utama. Sikap terbaik adalah?',
        'choices': [
            {'text': 'Menolak karena bukan jobdesk', 'is_correct': False},
            {'text': 'Bersedia membantu sesuai prioritas organisasi', 'is_correct': True},
            {'text': 'Menerima lalu menunda tanpa kabar', 'is_correct': False},
            {'text': 'Menyuruh orang lain menggantikan', 'is_correct': False},
        ]
    },
    {
        'text': 'Saat menemukan potensi konflik kepentingan dalam pekerjaan Anda akan?',
        'choices': [
            {'text': 'Mendiamkan agar pekerjaan cepat selesai', 'is_correct': False},
            {'text': 'Melaporkan sesuai prosedur dan menjaga objektivitas', 'is_correct': True},
            {'text': 'Membicarakan ke teman dekat saja', 'is_correct': False},
            {'text': 'Mengikuti arahan pihak yang diuntungkan', 'is_correct': False},
        ]
    },
]

for idx, q_data in enumerate(questions_tkp_cpns, 1):
    question, created = Question.objects.get_or_create(
        category=tkp_cpns,
        text=q_data['text'],
        defaults={'order': idx}
    )

    if created:
        for choice_data in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_data['text'],
                is_correct=choice_data['is_correct']
            )
        print(f"✓ Created question: {question.text}")
    else:
        print(f"✓ Question already exists: {question.text}")

print("\n" + "="*50)
print("✓ Data population complete!")
print("="*50)
print("\nTest Credentials:")
print("Username: testuser")
print("Password: test123")
print("\nAdmin Credentials:")
print("Username: admin")
print("Password: admin")
