from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

import django
from openpyxl import Workbook


django.setup()

from quiz.models import Category, Choice, Question


OUTPUT_DIR = Path('data/import')
HEADERS = [
    'parent_category',
    'category',
    'category_description',
    'question',
    'explanation',
    'image',
    'order',
    'choice_1',
    'choice_2',
    'choice_3',
    'choice_4',
    'choice_5',
    'correct_answer',
]


def row(
    order: int,
    question: str,
    choices: list[str],
    correct_answer: int,
    explanation: str,
) -> dict[str, object]:
    padded_choices = choices + [''] * (5 - len(choices))
    return {
        'parent_category': 'CPNS',
        'category': 'TKP 2024',
        'category_description': 'Tes Karakteristik Pribadi CPNS 2024',
        'question': question,
        'explanation': explanation,
        'image': '',
        'order': order,
        'choice_1': padded_choices[0],
        'choice_2': padded_choices[1],
        'choice_3': padded_choices[2],
        'choice_4': padded_choices[3],
        'choice_5': padded_choices[4],
        'correct_answer': correct_answer,
    }


ROWS = [
    row(1, 'Saat melayani pelanggan, seorang ibu menyerobot antrean dan meminta dilayani segera karena sudah terlalu lama menunggu. Sikap Anda ....', [
        'Memintanya untuk kembali ke antrean.',
        'Membiarkan saja karena ia tampak lelah.',
        'Meminta izin pada antrean yang ia lewati untuk melayaninya terlebih dahulu agar tidak terjadi keributan.',
        'Mendiamkan dan tidak mempedulikannya.',
        'Meminta teman untuk melayaninya.',
    ], 3, 'Pendekatan terbaik adalah menenangkan situasi tanpa membuat keributan, sambil tetap menghargai pihak lain yang sudah mengantre.'),
    row(2, 'Salah satu pengunjung komplain terhadap pelayanan yang diberikan oleh instansi tempat saya bekerja. Saya akan ....', [
        'Membantu menyelesaikan permasalahan pengunjung tersebut.',
        'Mengabaikan karena saya sedang banyak pekerjaan.',
        'Memberikan informasi akun dan kartu pendaftaran akun saja.',
        'Menjelaskan aturan dan prosedur yang berlaku.',
        'Menerima keluhan itu sebagai masukan dan menindaklanjutinya agar pelayanan membaik.',
    ], 5, 'Keluhan pelanggan adalah kritik dan saran yang penting untuk perbaikan layanan di masa depan.'),
    row(3, 'Saat saya dan teman saya sedang melakukan pelayanan, tiba-tiba seorang ibu marah-marah karena pelayanan yang tidak sesuai dan memarahi teman saya sampai menyakiti hatinya. Sikap Anda ....', [
        'Diam saja karena bukan urusan saya.',
        'Menenangkan ibu itu sambil tetap melayaninya dengan baik.',
        'Menenangkan ibu itu sambil menjelaskan bahwa ucapannya menyakiti hati teman saya.',
        'Menenangkan ibu itu dan meminta maaf.',
        'Marah dan mengajak teman untuk tidak melayani ibu itu.',
    ], 2, 'Dalam situasi konflik pelayanan, ketenangan dan fokus pada penyelesaian masalah adalah respons terbaik.'),
    row(4, 'Saat saya sedang melakukan pelayanan di kantor, teman masa kecil saya datang tiba-tiba dan tampaknya ingin bercerita panjang. Saya akan ....', [
        'Mengabaikannya karena saya tidak ingin bertemu teman saya.',
        'Meminta izin atasan supaya saya bisa menemuinya sekarang.',
        'Meminta teman saya menunggu sebentar.',
        'Menutup pelayanan sebentar untuk menemuinya.',
        'Meminta teman saya menunggu sampai saya menyelesaikan pelayanan.',
    ], 5, 'Profesionalisme menuntut kita menyelesaikan tanggung jawab pelayanan terlebih dahulu sebelum urusan pribadi.'),
    row(5, 'Seorang pelanggan ingin mengurus sesuatu dengan cepat. Teman Anda kelelahan dan butuh istirahat, sementara Anda masih memiliki tugas yang belum selesai. Sikap Anda ....', [
        'Menggantikan teman Anda untuk mengurusi pelanggan tersebut.',
        'Melanjutkan tugas teman yang kelelahan supaya kantor tidak terbengkalai.',
        'Melapor kepada atasan untuk meminta petunjuk.',
        'Melayani pelanggan dengan tenang walau bukan tugas Anda.',
        'Menyelesaikan tugas Anda sampai selesai, lalu membantu teman yang kelelahan.',
    ], 5, 'Tanggung jawab utama tetap harus diselesaikan, namun setelah itu kita tetap tanggap membantu rekan kerja yang membutuhkan.'),
    row(6, 'Saat melakukan pelayanan, hal utama yang saya perhatikan adalah ....', [
        'Kecepatan pelayanan.',
        'Kesesuaian prosedur.',
        'Kepuasan pelanggan.',
        'Keramahan pelayanan.',
        'Keuntungan instansi.',
    ], 3, 'Dalam pelayanan publik, orientasi utama adalah kepuasan pelanggan sebagai penerima layanan.'),
    row(7, 'Ketika menghadapi komplain atau keluhan pelanggan mengenai pelayanan di tempat kerja saya, saya akan ....', [
        'Mencatat dan menyampaikan keluhan tersebut pada atasan saya.',
        'Mencoba membantu pelanggan menyelesaikan persoalan.',
        'Mengabaikan karena kondisi saya memang seperti itu.',
        'Menjelaskan peran saya dalam menangani keluhan pelanggan.',
        'Menjelaskan aturan dan prosedur yang berlaku pada pelanggan.',
    ], 2, 'Tujuan utama pelayanan adalah membantu menyelesaikan masalah yang dikeluhkan pelanggan.'),
    row(8, 'Sebagai pelayan masyarakat, hal yang saya lakukan untuk meningkatkan kualitas kinerja saya adalah ....', [
        'Melayani dengan ramah.',
        'Memberikan informasi sebanyak mungkin.',
        'Bertindak proaktif dalam pelayanan.',
        'Melayani dengan ikhlas.',
        'Menjaga perasaan supaya tidak mudah emosi.',
    ], 3, 'Sikap proaktif menunjukkan kemauan memperbaiki mutu pelayanan secara nyata.'),
    row(9, 'Saya bekerja di sebuah apotek sebagai bagian penjualan. Saat apoteker belum datang, ada seseorang yang ingin membeli obat racik yang kebutuhannya mendesak. Saya akan ....', [
        'Meminta pertimbangan rekan kerja yang lain.',
        'Mencoba menghubungi apoteker dan menanyakan waktu kedatangannya.',
        'Langsung membuatkan obat racik karena kasihan.',
        'Memintanya untuk menunggu apoteker datang.',
        'Menjelaskan bahwa apoteker belum datang.',
    ], 2, 'Pada bidang kesehatan, prosedur dan kewenangan profesi harus tetap dipatuhi walaupun kebutuhan pelanggan mendesak.'),
    row(10, 'Menurut saya kunci utama keberhasilan sebuah tim dalam dunia kerja adalah ....', [
        'Pimpinan yang tegas.',
        'Koneksi dan komunikasi yang baik antar anggota tim.',
        'Kemauan seluruh anggota tim untuk bekerja keras.',
        'Semangat bersama untuk meraih keberhasilan.',
        'Kesamaan visi dan misi antar anggota tim.',
    ], 5, 'Tim yang tidak memiliki visi dan misi yang sama akan sulit mencapai hasil optimal.'),
    row(11, 'Menurut saya, cara paling mudah yang dapat dilakukan untuk mendapatkan jaringan kerja baru yang berkompeten adalah ....', [
        'Mencari dari lingkungan pertemanan dekat.',
        'Mencari dari lingkungan keluarga.',
        'Mencari dari lingkup profesional.',
        'Mencari dari kelompok minat yang sama dengan saya.',
        'Mencari dari alumni tempat saya kuliah.',
    ], 3, 'Lingkup profesional biasanya memberi akses yang lebih relevan dan kompeten untuk membangun jaringan kerja.'),
    row(12, 'Jika ada rekan kerja yang hendak pulang ketika tanggung jawabnya belum selesai, sikap saya yang paling tepat adalah ....', [
        'Pulang pada jam yang telah ditentukan.',
        'Mengikuti rekan kerja pulang pada jam yang sama.',
        'Melaporkan kejadian tersebut pada pimpinan.',
        'Mengingatkan rekan kerja tersebut agar bertanggung jawab dan menyelesaikan pekerjaannya dengan baik.',
        'Membiarkan rekan kerja pulang dan menyelesaikan pekerjaannya sendiri.',
    ], 4, 'Profesionalisme menuntut kita menjaga tanggung jawab kerja dan mengingatkan rekan dengan cara yang tepat.'),
    row(13, 'Cara efektif yang dapat dilakukan untuk memelihara hubungan kerja dengan relasi dan pelanggan adalah ....', [
        'Memberikan mereka banyak hadiah.',
        'Memberikan servis yang sangat baik.',
        'Memberikan diskon pada saat mereka melakukan pembelian.',
        'Menganggap mereka sebagai keluarga dan tidak sekadar pelanggan.',
        'Membina hubungan baik dengan pelanggan melalui komunikasi yang sehat dan berkelanjutan.',
    ], 5, 'Hubungan kerja yang baik dibangun melalui komunikasi, diskusi, dan perhatian terhadap kebutuhan pelanggan.'),
    row(14, 'Saat pembayaran uang lembur, saya mendapatkan uang lembur yang melebihi jam kerja lembur saya. Saya akan ....', [
        'Menanyakannya kepada bendahara.',
        'Mengembalikan kepada bendahara.',
        'Menerimanya dan menganggapnya sebagai bonus.',
        'Meminta pendapat teman apa yang harus dilakukan.',
        'Menerimanya dan pura-pura tidak tahu.',
    ], 2, 'Mengambil sesuatu yang bukan hak kita adalah tindakan yang tidak benar, sehingga harus dikembalikan.'),
    row(15, 'Seseorang menawarkan saya kenaikan jabatan, namun saya harus mempersiapkan sejumlah uang sebagai imbalannya. Saya akan ....', [
        'Tidak menerima peluang tersebut karena saya tidak memiliki uang.',
        'Meminta bantuan dari saudara.',
        'Mencari pinjaman keuangan.',
        'Mencari uang tambahan dari luar kantor.',
        'Tidak menerimanya dan tetap bekerja seperti biasa.',
    ], 5, 'Jabatan yang diperoleh lewat imbalan tidak sejalan dengan integritas dan tidak layak diterima.'),
    row(16, 'Tantangan dalam dunia kerja menurut saya adalah ....', [
        'Sesuatu yang cukup dipikirkan oleh atasan saja.',
        'Sebuah hal biasa.',
        'Hal yang memacu kita untuk berkembang.',
        'Sesuatu yang dapat menghancurkan kita.',
        'Sesuatu yang bisa dihindari dengan bekerja cermat.',
    ], 3, 'Tantangan justru dapat menjadi pendorong untuk belajar dan berkembang lebih baik.'),
    row(17, 'Sebagai wedding organizer, saya mendapatkan klien yang meminta pernikahan dengan budaya asal mereka yang sulit dipenuhi karena jauh dari tempat saya tinggal. Saya akan ....', [
        'Menyarankan mereka memakai baju adat daerah saya saja karena lebih mudah didapatkan.',
        'Menyarankan mereka memakai pakaian nasional saat resepsi.',
        'Memenuhi semua permintaan mereka menggunakan budaya asal mereka.',
        'Memenuhi permintaan itu dengan syarat semua perlengkapan disiapkan oleh mereka.',
        'Menghubungi rekan wedding organizer dari daerah asal mereka untuk membantu saya.',
    ], 5, 'Mencari bantuan profesional yang lebih dekat dengan sumber kebutuhan adalah solusi paling efektif dan menghargai keinginan klien.'),
    row(18, 'Dalam rapat RT diusulkan supaya seluruh warga kerja bakti membantu pembangunan gedung pertemuan RT yang sedang dikerjakan kontraktor berpengalaman. Menurut saya ....', [
        'Memenuhi semua permintaan mereka untuk menggunakan budaya yang sudah dikerjakan oleh ahlinya.',
        'Lebih baik kerja bakti dilakukan untuk kebersihan lingkungan saja.',
        'Membiarkan kontraktor tetap bekerja tanpa keterlibatan warga.',
        'Penting untuk mempererat kebersamaan antarwarga RT.',
        'Penting untuk menumbuhkan rasa memiliki warga RT terhadap fasilitas gedung pertemuan tersebut.',
    ], 2, 'Pekerjaan teknis sebaiknya dilakukan sesuai bidang ahlinya, sehingga peran warga lebih tepat diarahkan pada hal yang relevan.'),
    row(19, 'Menurut saya dalam bersosialisasi dengan tetangga dan di dalam masyarakat umum seharusnya kita ....', [
        'Bersikap aktif dan memberikan peran positif pada mereka.',
        'Apa adanya sesuai kepribadian saya.',
        'Bersikap pasif dan menunggu untuk diajak terlebih dahulu.',
        'Bersosialisasi seperlunya saja.',
        'Menempatkan diri sesuai kondisi lingkungan yang ada.',
    ], 1, 'Bersosialisasi yang baik membutuhkan sikap aktif dan kontribusi positif dalam lingkungan.'),
    row(20, 'Dalam acara bersama disajikan makanan khas daerah yang sebenarnya tidak saya sukai. Yang saya lakukan adalah ....', [
        'Membeli menu makanan sendiri supaya tidak memberatkan panitia.',
        'Memakan menu yang disajikan porsi sedikit saja untuk menghormati.',
        'Menolak dengan jujur karena saya tidak suka.',
        'Meminta panitia menyiapkan menu khusus dengan uang pribadi saya.',
        'Menghargai makanan yang disajikan kepada saya tanpa meragukannya.',
    ], 5, 'Menghargai pemberian orang lain adalah cara menjaga hubungan baik dalam interaksi sosial.'),
    row(21, 'Pertemuan RT di lingkungan saya akan diadakan di rumah orang yang sedang bermasalah dengan saya. Sikap saya ....', [
        'Tetap menghadiri pertemuan RT tersebut seperti biasa.',
        'Tetap menghadiri pertemuan dan menggunakan kesempatan itu untuk mengklarifikasi secara terbuka.',
        'Tetap menghadiri pertemuan RT tersebut seperti biasa dan menjaga hubungan tetap baik.',
        'Tidak menghadiri pertemuan RT tersebut.',
        'Hadir sebentar saja dalam pertemuan RT tersebut.',
    ], 3, 'Dalam bersosialisasi, kita perlu menjaga hubungan baik dan tetap hadir secara profesional dalam kegiatan bersama.'),
    row(22, 'Anda sedang terburu-buru pergi ke kantor karena ada rapat mendadak dengan atasan, tetapi Anda mendapati piring pecah di lantai dapur yang dapat membahayakan orang lain. Tindakan Anda ....', [
        'Membiarkannya saja dan tetap buru-buru berangkat.',
        'Menelepon teman untuk menggantikan rapat.',
        'Memenuhi semua permintaan mereka untuk menggunakan budaya tertentu.',
        'Membersihkan pecahan itu lalu berangkat dengan cepat.',
        'Menutup pecahan dengan kain agar tidak tampak.',
    ], 4, 'Profesionalisme juga mencakup tanggung jawab terhadap keselamatan orang lain sebelum meninggalkan rumah.'),
    row(23, 'Saat sedang merayakan ulang tahun, datang kabar bahwa rekan Anda mengalami kecelakaan. Maka Anda akan ....', [
        'Membatalkan pesta ulang tahun dan bergegas ke rumah sakit.',
        'Memberinya bantuan semampu Anda.',
        'Mengkoordinasikan rekan-rekan lain untuk turut membantu.',
        'Melaporkan kepada pihak berwajib tentang hal ini.',
        'Memenuhi semua permintaan mereka untuk menggunakan budaya tertentu.',
    ], 2, 'Dalam pertemanan, membantu sesuai kemampuan secara cepat adalah sikap yang baik dan proporsional.'),
    row(24, 'Di perusahaan Anda baru saja memperbarui salah satu perangkat IT guna mempermudah karyawan menyelesaikan tugasnya. Sikap Anda adalah ....', [
        'Mempelajari perangkat tersebut sendiri di waktu luang.',
        'Mencari informasi mengenai pengoperasian perangkat tersebut bersama rekan-rekan Anda.',
        'Meminta orang lain untuk mengajar Anda dan rekan-rekan cara mengoperasikan perangkat tersebut.',
        'Mencari informasi di internet dan mempelajarinya bersama rekan-rekan Anda.',
        'Mengajak rekan-rekan mencari informasi terkait pengoperasian perangkat tersebut sepulang jam kantor.',
    ], 4, 'Sikap paling baik adalah proaktif belajar dan berbagi pengetahuan agar perubahan teknologi langsung mendukung pekerjaan.'),
    row(25, 'Anda melakukan kesalahan fatal dalam tugas karena kurangnya pemahaman tentang teknologi informasi. Yang Anda lakukan ....', [
        'Mencari jalan keluar dari permasalahan yang saya hadapi.',
        'Menunggu pengarahan tentang pentingnya teknologi informasi.',
        'Membahas permasalahan yang saya hadapi dengan rekan kerja saya.',
        'Melapor pada atasan dan mulai mengikuti petunjuknya.',
        'Menyalahkan sistem yang digunakan.',
    ], 3, 'Belajar langsung dari orang yang lebih paham dan membahas masalah secara terbuka adalah respons yang tepat untuk berkembang.'),
    row(26, 'Kemajuan IT menuntut Anda untuk membuat sistem baru di perusahaan. Sikap Anda ....', [
        'Menunggu sampai perusahaan mengajari Anda secara resmi.',
        'Belajar langsung kepada ahli IT di perusahaan Anda dan ikut mengembangkan sistem tersebut.',
        'Tidak ikut andil dalam pengembangan teknologi yang ada.',
        'Ikut mengembangkan teknologi tersebut bersama ahli IT dan membantu menggerakkan anggota lain.',
        'Menerima teknologi baru tersebut lalu mengolaborasikannya dengan ide Anda.',
    ], 2, 'Dari pembahasan sumber, sikap terbaik adalah belajar langsung kepada ahli IT dan aktif ikut mengembangkan sistem yang dibutuhkan.'),
    row(27, 'Anda sedang mengerjakan tugas dengan suatu aplikasi. Tiba-tiba di tengah jalan aplikasi tersebut error sehingga mengganggu pekerjaan. Anda akan ....', [
        'Langsung menutup aplikasi tersebut agar data tidak semakin hilang.',
        'Memanggil ahli IT dan menanyakan keadaannya.',
        'Menanyakan kepada teman yang pernah mengalami hal serupa.',
        'Terus mengerjakan dan berharap aplikasi kembali normal.',
        'Menyampaikan pada atasan dan meminta nasihat.',
    ], 1, 'Langkah pertama yang paling aman adalah mencegah kerusakan bertambah besar sebelum mengambil tindakan lanjutan.'),
    row(28, 'Atasan meminta saya membuat laporan hasil kerja melalui aplikasi berbasis internet, sementara saya terbiasa membuat laporan dengan print out hasil ketikan komputer. Saya akan ....', [
        'Tetap menggunakan cara lama yang saya kuasai.',
        'Mengeluh karena belum terbiasa menggunakan aplikasi.',
        'Belajar membuat laporan hasil kerja melalui aplikasi.',
        'Meminta agar saya tidak dipaksa menggunakan aplikasi.',
        'Malas membuat laporan hasil kerja.',
    ], 3, 'Dalam dunia kerja, kita perlu mengikuti perkembangan alat kerja dan terus belajar agar tidak tertinggal.'),
    row(29, 'Ketika menghadapi banyak masalah dalam pekerjaan secara bersamaan, sikap saya adalah ....', [
        'Sabar dan berusaha menghadapi masalah tersebut.',
        'Berdoa, pasrah diri, dan berusaha melupakan masalah.',
        'Berusaha menyelesaikan masalah satu per satu.',
        'Meminta bantuan teman untuk menyelesaikan semua masalah.',
        'Membiarkan masalah berlalu dengan sendirinya.',
    ], 3, 'Masalah akan lebih mudah diatasi jika dipilah dan diselesaikan secara bertahap satu per satu.'),
    row(30, 'Tetangga saya sering membuang sampah di halaman rumah saya. Yang saya lakukan adalah ....', [
        'Memarahinya saat ia datang membuang sampah.',
        'Melaporkannya kepada ketua RT.',
        'Mendatanginya dan memintanya untuk tidak membuang sampah sembarangan.',
        'Membalas dengan membuang sampah di halamannya.',
        'Memberi tanda peringatan untuk tidak membuang sampah di halaman.',
    ], 3, 'Komunikasi langsung yang baik dan tanpa emosi adalah langkah paling tepat sebelum eskalasi.'),
    row(31, 'Untuk memenuhi target yang diberikan pada kelompok saya, saya ....', [
        'Memberikan kontribusi ala kadarnya saja.',
        'Memberikan kontribusi yang maksimal agar target terpenuhi.',
        'Memberikan kontribusi yang minimal karena kegagalan ditanggung bersama.',
        'Bekerja sama dengan baik dengan anggota kelompok lain.',
        'Segera menentukan target pribadi dan tidak memikirkan target anggota lain.',
    ], 2, 'Dalam kerja kelompok, setiap orang perlu memberi kontribusi terbaik agar target bersama tercapai.'),
    row(32, 'Saat saya dipercaya sebagai petugas dalam promo penjualan produk baru, saya melihat antrean sangat banyak, tidak teratur, dan berebut mendapatkan pelayanan. Maka saya ....', [
        'Menertibkan dan berinisiatif membuat nomor antrean.',
        'Memarahi calon pembeli yang tidak mau mengalah.',
        'Memperhatikan saja.',
        'Melapor kepada pimpinan untuk segera bertindak.',
        'Menertibkan dan berinisiatif membuka loket tambahan jika memungkinkan.',
    ], 1, 'Kita harus mampu membaca situasi dan mengambil tindakan efisien untuk mengatasi masalah langsung di lapangan.'),
    row(33, 'Seseorang datang meminta pelayanan tetapi syarat-syaratnya belum lengkap. Saya akan ....', [
        'Menolak dan memintanya kembali saat syaratnya sudah lengkap.',
        'Melihat syarat apa saja yang kurang, barangkali masih bisa diberi pelayanan.',
        'Berkonsultasi dengan atasan atau pihak yang berwenang apakah ada kebijakan yang bisa diberikan.',
        'Langsung memberinya pelayanan karena kasihan.',
        'Langsung memberinya pelayanan karena ia datang dari jauh.',
    ], 3, 'Jika persoalan berada di luar kewenangan kita, langkah terbaik adalah berkonsultasi dengan pihak yang berkompeten.'),
    row(34, 'Sebagai seorang jurnalis, saya ditugaskan meliput daerah yang terkena bencana alam gunung meletus. Hal yang saya lakukan ....', [
        'Menjalankan tugas dan mencari informasi keadaan daerah yang akan saya liput.',
        'Menjalankan tugas dengan catatan semua perlengkapan sudah tersedia.',
        'Memenuhi semua permintaan mereka untuk menggunakan budaya tertentu.',
        'Meminta atasan untuk mengganti tugas saya.',
        'Menolak tugas tersebut dengan sopan.',
    ], 2, 'Sebelum bertugas di lokasi berbahaya, kesiapan perlengkapan dan kondisi kerja harus dipastikan lebih dahulu.'),
    row(35, 'Guna menghalau efek negatif dari media sosial, apa yang Anda lakukan ....', [
        'Tidak mengubris apabila ada yang berkata kasar di media sosial.',
        'Mempunyai dua akun media sosial.',
        'Membuat media sosial dengan nama samaran.',
        'Menggunakan media sosial untuk hal yang bermanfaat dan menyortir penggunaannya.',
        'Hanya menggunakan media sosial tertentu saja.',
    ], 4, 'Cara terbaik adalah menggunakan media sosial secara bijak dan menyortir dampak negatifnya.'),
    row(36, 'Saat Anda berada di bandara dan segera harus naik pesawat, Anda melihat seorang nenek kebingungan. Bagaimana sikap Anda?', [
        'Membantu nenek tersebut menyelesaikan masalahnya.',
        'Meminta bantuan satpam atau petugas bandara untuk membantu nenek tersebut.',
        'Segera menuju pesawat dan berharap ada orang lain yang menolongnya.',
        'Bertanya dulu kepada nenek tersebut, lalu bila sangat penting saya akan membantunya.',
        'Meminta jasa orang lain yang profesional untuk membantu nenek tersebut.',
    ], 2, 'Karena Anda harus segera naik pesawat, solusi terbaik adalah segera meminta bantuan petugas yang tepat agar nenek itu tetap tertolong.'),
    row(37, 'Ada rumor bahwa seorang pegawai telah menggelapkan uang perusahaan, tetapi informasinya belum pasti. Sikap Anda ....', [
        'Pihak perusahaan harus memberikan sanksi tegas kepada pelaku.',
        'Menanyakan kebenaran informasi tersebut kepada rekan kerja Anda.',
        'Tidak berkomentar lebih jauh sebelum ada kepastian informasi.',
        'Pelaku sangat di luar batas dan menyebabkan kerugian besar.',
        'Mendatangi rumah pegawai yang dituduh.',
    ], 3, 'Sikap profesional menuntut kita tidak terburu-buru menyebarkan atau menilai kabar yang belum pasti kebenarannya.'),
    row(38, 'Perusahaan tempat Anda bekerja menuntut pegawai dapat menguasai bahasa asing. Agar semua pegawai dapat mengikuti kursus tanpa mengganggu kerja instansi, sebagai panitia Anda akan ....', [
        'Menyelenggarakan kursus di hari libur.',
        'Menyelenggarakan kursus pada jam istirahat.',
        'Menyelenggarakan kursus setelah jam kantor selesai.',
        'Menyelenggarakan kursus secara bertahap agar tidak mengganggu kinerja instansi.',
        'Meminta pendapat rekan-rekan kapan sebaiknya kursus dilaksanakan.',
    ], 4, 'Walau pada sumber cetak tertulis jawaban lain, tabel skor dan pembahasan jelas mengarahkan pada pelaksanaan bertahap agar pekerjaan tidak terganggu.'),
    row(39, 'Anda adalah karyawan dengan dedikasi tinggi terhadap pekerjaan. Suatu hari Anda dihadapkan pada banyak pekerjaan dengan deadline yang berdekatan. Maka Anda akan ....', [
        'Pulang sesuai jadwal dan meninggalkan pekerjaan untuk esok hari.',
        'Memilih lembur demi tambahan uang lembur.',
        'Menyelesaikan pekerjaan sesuai deadline dengan hasil sebisanya.',
        'Melapor kepada atasan bahwa Anda membutuhkan bantuan karyawan lain untuk menangani banyaknya tugas.',
        'Membawa tugas ke rumah dan mengerjakannya sampai larut malam.',
    ], 4, 'Dalam kondisi pekerjaan menumpuk, komunikasi kepada atasan tentang kebutuhan dukungan adalah langkah yang paling profesional dan realistis.'),
    row(40, 'Terjadi konflik antar dua suku karena salah satu pihak merasa dihina. Salah satu upaya pemerintah yang tepat untuk melerai konflik tersebut adalah ....', [
        'Menumpuk kesadaran toleransi antar suku.',
        'Melakukan mediasi terhadap kedua suku.',
        'Mencegah kedua suku tersebut bertikai.',
        'Menangkap pelaku yang menjadi pemicu perkelahian.',
        'Membiarkan mereka menyelesaikan sendiri konfliknya.',
    ], 2, 'Dalam konflik sosial yang sedang memanas, mediasi adalah langkah paling tepat untuk meredakan dan membuka ruang penyelesaian.'),
    row(41, 'Negara Indonesia memiliki beragam latar belakang. Agar tercipta kerukunan antarumat beragama, semua umat beragama hendaknya ....', [
        'Mengganti ideologi negara yang baru.',
        'Lebih serius mempelajari ajaran agamanya.',
        'Menciptakan satu hukum agama untuk semua umat.',
        'Mengedepankan sikap saling menghormati dan menghargai.',
        'Menghayati semua ajaran agama yang ada.',
    ], 4, 'Kerukunan antarumat beragama dibangun dengan saling menghormati dan menghargai perbedaan.'),
    row(42, 'Di masa kampanye terjadi konflik antarpartisipan pendukung karena merasa calon yang didukung paling benar dan menjelekkan pihak lain. Berdasarkan kasus tersebut, konflik terjadi karena ....', [
        'Adanya persaingan, pertentangan, dan kontroversi antar pihak.',
        'Norma-norma sosial sudah tidak berfungsi dengan baik.',
        'Sanksi terhadap pelanggaran norma tidak tegas atau lemah.',
        'Adanya pertentangan norma yang membingungkan.',
        'Adanya kesenjangan ekonomi yang telah lama terjadi.',
    ], 1, 'Pembahasan sumber mengarah pada konflik yang timbul dari persaingan dan pertentangan antar kelompok untuk mencapai tujuan tertentu.'),
    row(43, 'Anda memiliki sahabat yang berbeda agama dan sedang merayakan hari besar keagamaannya. Sikap yang perlu Anda tunjukkan yaitu ....', [
        'Menghormati keyakinan agama yang dianut sahabat tersebut.',
        'Menjaga ketenangan selama pelaksanaan hari raya agar berjalan lancar.',
        'Ikut merayakan hari besar agamanya karena ia sahabat Anda.',
        'Tidak perlu melakukan apa-apa karena itu bukan agama Anda.',
        'Membiarkannya selama tidak mengganggu Anda.',
    ], 2, 'Bentuk konkret sikap kebersamaan yang tepat adalah menjaga ketenangan dan menghormati pelaksanaan ibadah tanpa melanggar keyakinan sendiri.'),
    row(44, 'Salah satu rekan kantor berubah menjadi tertutup dan mulai menganggap orang yang tidak sejalan dengannya sebagai sesat. Menghadapi perubahan sikap rekan tersebut, apa yang Anda lakukan ....', [
        'Tidak melakukan apa-apa karena itu bukan urusan saya.',
        'Membiarkannya dikerjakan oleh kontraktor berpengalaman.',
        'Mengajaknya berdiskusi dan meluruskan jalan pikirannya.',
        'Melaporkan kepada atasan.',
        'Melaporkan kepada polisi.',
    ], 4, 'Karena masih berada dalam ruang lingkup kantor, atasan adalah pihak yang paling tepat untuk mengambil tindakan lebih lanjut.'),
]


def export_rows(rows: list[dict[str, object]]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / 'cpns_tkp_2024_final.csv'
    xlsx_path = OUTPUT_DIR / 'cpns_tkp_2024_final.xlsx'

    with csv_path.open('w', newline='', encoding='utf-8-sig') as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Questions'
    sheet.append(HEADERS)
    for item in rows:
        sheet.append([item[key] for key in HEADERS])
    workbook.save(xlsx_path)
    workbook.close()
    return csv_path, xlsx_path


def sync_to_database(rows: list[dict[str, object]]) -> None:
    parent_category, _ = Category.objects.get_or_create(
        name='CPNS',
        parent=None,
        defaults={'description': 'Kategori utama soal CPNS.'},
    )
    category, _ = Category.objects.get_or_create(
        name='TKP 2024',
        parent=parent_category,
        defaults={'description': 'Tes Karakteristik Pribadi CPNS 2024'},
    )
    category.description = 'Tes Karakteristik Pribadi CPNS 2024'
    category.save(update_fields=['description'])

    for item in rows:
        question, _ = Question.objects.update_or_create(
            category=category,
            order=item['order'],
            defaults={
                'text': item['question'],
                'explanation': item['explanation'],
            },
        )
        if question.image:
            question.image.delete(save=False)
            question.image = None
            question.save(update_fields=['image'])

        question.choices.all().delete()
        for index in range(1, 6):
            choice_text = item[f'choice_{index}']
            if not choice_text:
                continue
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=item['correct_answer'] == index,
            )


def main() -> None:
    csv_path, xlsx_path = export_rows(ROWS)
    sync_to_database(ROWS)
    print(f'Exported CSV: {csv_path}')
    print(f'Exported XLSX: {xlsx_path}')
    print(f'Synced {len(ROWS)} questions into category CPNS > TKP 2024')


if __name__ == '__main__':
    main()
