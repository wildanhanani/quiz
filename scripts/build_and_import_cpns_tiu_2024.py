from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

import django
from django.core.files import File
from openpyxl import Workbook
from PIL import Image


django.setup()

from quiz.models import Category, Choice, Question


OUTPUT_DIR = Path('data/import')
IMAGE_SOURCE_DIR = Path('data/rendered/tiu_2024')
IMAGE_EXPORT_DIR = OUTPUT_DIR / 'cpns_tiu_2024_images'
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
    image: str = '',
) -> dict[str, object]:
    padded_choices = choices + [''] * (5 - len(choices))
    return {
        'parent_category': 'CPNS',
        'category': 'TIU 2024',
        'category_description': 'Tes Intelegensia Umum CPNS 2024',
        'question': question,
        'explanation': explanation,
        'image': image,
        'order': order,
        'choice_1': padded_choices[0],
        'choice_2': padded_choices[1],
        'choice_3': padded_choices[2],
        'choice_4': padded_choices[3],
        'choice_5': padded_choices[4],
        'correct_answer': correct_answer,
    }


ROWS = [
    row(1, 'BECAK : KENDARAAN = .... : ....', ['Gadis : Orang', 'Bengawan : Sungai', 'Guru : Murid', 'Baja : Belati', 'Kapal : Perahu'], 1, 'Hubungannya adalah bagian terhadap keseluruhan. Becak merupakan bagian dari kendaraan, sebagaimana gadis merupakan bagian dari orang.'),
    row(2, 'HEINA : ANJING HUTAN = .... : ....', ['Anoa : Macan', 'Luwak : Burung', 'Kuwuk : Kambing', 'Bajing : Kucing', 'Keluai : Musang'], 5, 'Heina adalah nama lain dari anjing hutan. Keluai adalah nama lain dari musang.'),
    row(3, 'CHILI : SANTIAGO = .... : ....', ['Indonesia : Denpasar', 'Srilanka : Colombo', 'Nairobi : Kenya', 'Mesir : Tripoli', 'Maroko : Tunis'], 2, 'Hubungannya adalah negara dan ibu kota. Chili beribu kota Santiago, sedangkan Srilanka beribu kota Colombo.'),
    row(4, 'TANGAN BESI : BERPERILAKU KERAS = .... : ....', ['Panjang usus : Kecewa', 'Buah bibir : Kehormatan', 'Kepala batu : Supel', 'Panas hati : Marah', 'Mata-mata : Tangan kaki'], 4, 'Kiasan tangan besi berarti berperilaku keras. Kiasan panas hati berarti marah.'),
    row(5, 'X, U, X, R, X, O, X, ....', ['L', 'N', 'K', 'X', 'M'], 1, 'Huruf X tetap, sedangkan huruf di antaranya mundur tiga langkah: U, R, O, L.'),
    row(6, 'ABD, FGI, KLN, PQS, ....', ['WXA', 'UVW', 'TUV', 'TUW', 'UVX'], 5, 'Tiap kelompok maju dengan pola +1, +2 di dalam kelompok dan loncatan antar kelompok yang konsisten, sehingga lanjutan yang tepat adalah UVX.'),
    row(7, '23, 26, 19, 22, 15, 18, ...., ....', ['21 dan 14', '21 dan 24', '11 dan 18', '11 dan 4', '11 dan 14'], 5, 'Polanya +3 lalu -7 secara bergantian: 23, 26, 19, 22, 15, 18, 11, 14.'),
    row(8, 'C, G, K, O, ...., ....', ['T dan X', 'S dan V', 'S dan W', 'R dan V', 'R dan W'], 3, 'Pola huruf bertambah empat langkah: C, G, K, O, S, W.'),
    row(9, 'Hanya senapati agung yang memimpin prajurit Singasari dalam peperangan. Pangeran Singasari tidak tunduk pada perintah senapati agung. Pernyataan yang sesuai adalah ....', ['Pangeran Singasari bukan prajurit Singasari dalam peperangan', 'Pangeran Singasari diperbolehkan memimpin prajurit Singasari dalam peperangan', 'Senapati agung tunduk pada perintah pangeran Singasari dalam peperangan', 'Pangeran Singasari tidak tunduk pada perintah senapati agung dalam peperangan', 'Tidak dapat ditarik kesimpulan'], 1, 'Jika semua prajurit Singasari tunduk pada senapati agung dalam peperangan, maka pihak yang tidak tunduk pada senapati agung bukan termasuk prajurit Singasari.'),
    row(10, 'Ikan kakap merah penampilannya menarik. Ikan tuna rasanya enak. Udang bergizi tinggi. Bandeng bergizi. Hidangan yang menarik dan bergizi adalah ....', ['Ikan tuna dan bandeng', 'Ikan kakap merah dan udang', 'Bandeng dan kakap merah', 'Udang dan bandeng', 'Ikan tuna dan kakap merah'], 2, 'Pada data yang diberikan, kakap merah memiliki sifat menarik dan udang memiliki sifat bergizi tinggi.'),
    row(11, 'Semua peserta CPNS menempuh tes kemampuan dasar. Sebagian peserta CPNS mengikuti tes kemampuan bidang. Jadi ....', ['Semua peserta CPNS yang menempuh tes kemampuan dasar tidak mengikuti tes kemampuan bidang', 'Semua peserta CPNS yang mengikuti tes kemampuan bidang tidak menempuh tes kemampuan dasar', 'Semua peserta CPNS yang tidak mengikuti tes kemampuan bidang tidak menempuh tes kemampuan dasar', 'Sebagian peserta CPNS yang tidak mengikuti tes kemampuan bidang menempuh tes kemampuan dasar', 'Sebagian peserta CPNS yang mengikuti tes kemampuan bidang tidak menempuh tes kemampuan dasar'], 4, 'Dari premis umum dan premis sebagian, kesimpulan partikular yang masih mungkin adalah sebagian peserta yang tidak mengikuti tes kemampuan bidang tetap menempuh tes kemampuan dasar.'),
    row(12, 'Semua murid yang mengikuti ujian tidak menggunakan kalkulator. Sebagian murid yang ujian mengenakan jam tangan. Jadi ....', ['Semua murid yang ujian mengenakan jam tangan', 'Sementara murid yang ujian tidak mengenakan jam tangan', 'Semua murid yang ujian tidak menggunakan kalkulator dan tidak mengenakan jam tangan', 'Sebagian murid yang ujian mengenakan jam tangan dan tidak menggunakan kalkulator', 'Sebagian murid yang ujian mengenakan jam tangan dan menggunakan kalkulator'], 4, 'Karena semua peserta ujian tidak menggunakan kalkulator dan sebagian dari mereka mengenakan jam tangan, maka sebagian murid ujian mengenakan jam tangan dan tidak menggunakan kalkulator.'),
    row(13, 'Semua mahasiswa berdasi. Sebagian mahasiswa berjas. Jadi ....', ['Sebagian mahasiswa berjas', 'Sebagian mahasiswa berjas dan bersepatu', 'Sebagian mahasiswa berdasi dan berjas', 'Sebagian mahasiswa berdasi, tapi berjas', 'Semua mahasiswa berdasi dan berjas'], 3, 'Dari satu premis umum dan satu premis sebagian, kesimpulan yang dapat diambil adalah sebagian mahasiswa berdasi dan berjas.'),
    row(14, 'Semua siswa kelas A dapat berbahasa Inggris. Sebagian siswa kelas A mendapat nilai tinggi. Jadi ....', ['Sebagian siswa kelas A mendapat nilai tinggi dan dapat berbahasa Inggris', 'Sebagian siswa kelas A mendapat nilai tinggi dan tidak dapat berbahasa Inggris', 'Sebagian siswa kelas A tidak mendapat nilai tinggi dan tidak dapat berbahasa Inggris', 'Sebagian siswa kelas A mendapat nilai tinggi tetapi tidak dapat berbahasa Inggris', 'Semua siswa kelas A tidak mendapat nilai tinggi dan dapat berbahasa Inggris'], 1, 'Karena semua siswa kelas A bisa berbahasa Inggris dan sebagian siswa kelas A mendapat nilai tinggi, maka sebagian siswa kelas A mendapat nilai tinggi dan dapat berbahasa Inggris.'),
    row(15, 'Ali lebih cermat dari Budi, tetapi lebih ceroboh dari Dani. Mardi lebih cermat dari Dani. Urutan dari yang paling cermat adalah ....', ['Mardi, Dani, Ali, Budi', 'Deni, Mardi, Ali, Budi', 'Mardi, Ali, Budi, Deni', 'Mardi, Deni, Budi, Ali', 'Deni, Budi, Mardi, Ali'], 1, 'Simbol hubungan memberi urutan Mardi > Dani > Ali > Budi.'),
    row(16, 'X lebih tua dari N, E lebih muda dari A, T lebih muda dari N, X lebih muda dari E, N lebih tua dari T, maka yang termuda adalah ....', ['N', 'E', 'X', 'T', 'A'], 4, 'Urutan dari tua ke muda adalah A, E, X, N, T. Jadi yang termuda adalah T.'),
    row(17, 'Jika A = B maka A tidak sama dengan C. Bila P = A maka ....', ['Bila P = C maka P = B', 'Bila P = C maka P tidak sama dengan A', 'Bila P = C maka P tidak sama dengan B', 'Bila P = C maka P = A = B', 'Bila P = C maka B bukan A'], 2, 'Jika A = B dan A tidak sama dengan C, maka bila P = C, P juga tidak sama dengan A.'),
    row(18, 'Jika x = luas persegi dengan panjang sisi 20 dan y = luas lingkaran dengan diameter 20 maka ....', ['x > y', 'x < y', 'x = y', 'x dan y tidak bisa ditentukan', 'x > 2y'], 1, 'Luas persegi 20 × 20 = 400. Luas lingkaran dengan jari-jari 10 sekitar 314. Maka x lebih besar dari y.'),
    row(19, 'Jika a = 4,5, b = 5,4 dan c = a + b² maka hasil (a² × b) − c adalah ....', ['76,59', '75,69', '75,96', '75,95', '74,59'], 2, 'Dari a = 4,5 dan b = 5,4 diperoleh c = 4,5 + 29,16 = 33,66. Nilai (a² × b) − c = 20,25 × 5,4 − 33,66 = 75,69.'),
    row(20, 'Seorang pedagang membeli barang seharga Rp450.000,00 lalu berhasil menjual semuanya seharga Rp573.750,00. Berapakah persentase keuntungan yang didapat pedagang tersebut?', ['20%', '22,5%', '25%', '25,5%', '27,5%'], 5, 'Keuntungan = 573.750 − 450.000 = 123.750. Persentase keuntungan = 123.750 / 450.000 × 100% = 27,5%.'),
    row(21, 'Jika keliling sebuah lingkaran 34,53 meter, berapakah jari-jarinya?', ['4,5 m', '5,5 m', '6,5 m', '7,5 m', '8,5 m'], 2, 'Keliling lingkaran 2 × π × r. Dengan π = 3,14 diperoleh r = 34,54 / 6,28 ≈ 5,5 meter.'),
    row(22, '(17 × 125 + 83 × 125) : 25 = ....', ['20', '200', '320', '500', '720'], 4, 'Gunakan distribusi: (17 + 83) × 125 ÷ 25 = 100 × 5 = 500.'),
    row(23, 'Jika 291ab − 32 = 328 maka 97ab = ....', ['120', '130', '140', '150', '160'], 1, 'Dari 291ab − 32 = 328 diperoleh 291ab = 360. Karena 291 = 3 × 97, maka 97ab = 120.'),
    row(24, '634 + 8 × 125 − 2.048 : 64 = ....', ['1.456', '1.602', '1.666', '1.774', '1.888'], 2, 'Kerjakan kali dan bagi lebih dahulu: 8 × 125 = 1.000 dan 2.048 ÷ 64 = 32. Hasil akhirnya 634 + 1.000 − 32 = 1.602.'),
    row(25, 'Nilai 37,5% dari 0,333 adalah ....', ['0,008', '0,015', '0,1', '0,125', '0,321'], 4, 'Pada sumber soal, 37,5% diperlakukan sebagai 3/8 dan hasil yang diinginkan adalah 0,125.'),
    row(26, 'Untuk dapat pergi ke Makassar seseorang dari Cilacap harus ke Jakarta lebih dahulu. Banyaknya kendaraan dari Cilacap ke Jakarta ada 6, dari Jakarta ke Makassar ada 4, dari Makassar ke Jakarta 4, dan dari Jakarta ke Cilacap 6. Jika saat pulang tidak boleh menggunakan kendaraan yang sama untuk rute yang sama, banyak cara pulang-pergi adalah ....', ['160', '200', '240', '360', '400'], 4, 'Pergi: 6 × 4 cara. Pulang: 3 × 5 cara karena kendaraan pada rute yang sama tidak boleh dipakai lagi. Total 6 × 4 × 3 × 5 = 360.'),
    row(27, 'Perbandingan usia orang tua dan anak muda adalah 3 : 1. Jika jumlah umur keduanya 36 tahun, perbandingan sembilan tahun kemudian adalah ....', ['3 : 1', '2 : 1', '3 : 2', '4 : 3', '5 : 4'], 2, 'Jika x : y = 3 : 1 dan x + y = 36, maka umur mereka 27 dan 9. Sembilan tahun kemudian menjadi 36 dan 18, sehingga perbandingannya 2 : 1.'),
    row(28, 'Sebuah balok memiliki perbandingan panjang : lebar : tinggi = 4 : 2 : 3. Jika panjang balok 12 cm, luas seluruh permukaan balok adalah ....', ['468 cm²', '516 cm²', '576 cm²', '624 cm²', '688 cm²'], 1, 'Dengan panjang 12 cm, maka lebar 6 cm dan tinggi 9 cm. Luas permukaan = 2(pl + pt + lt) = 2(72 + 108 + 54) = 468 cm².'),
    row(29, 'Perhatikan gambar pada lampiran soal. Seri gambar lanjutan dari pola gambar berikut adalah ....', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 5, 'Polanya berotasi 90 derajat searah jarum jam, berpindah ke sisi batas kotak berikutnya, dan setiap tahap menambah satu tanda yang lebih besar.', image='tiu-2024-q29.png'),
    row(30, 'Perhatikan gambar pada lampiran soal. Seri gambar lanjutan dari pola gambar berikut adalah ....', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 4, 'Dalam tiap langkah, elemen yang ada membesar lalu muncul elemen baru di dalamnya. Pilihan yang sesuai adalah gambar keempat.', image='tiu-2024-q30.png'),
    row(31, 'Perhatikan gambar pada lampiran soal. Carilah gambar yang berbeda dari yang lainnya.', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 1, 'Semua gambar terbagi menjadi empat bagian. Gambar pertama berbeda karena bagian yang diarsir berada di kanan atas, sedangkan yang lain di kanan bawah.', image='tiu-2024-q31.png'),
    row(32, 'Perhatikan gambar pada lampiran soal. Carilah gambar yang berbeda dari yang lainnya.', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 4, 'Pada semua pilihan lain, jumlah titik di luar gambar utama hanya lebih satu dibanding jumlah titik di dalamnya. Gambar keempat berbeda karena selisihnya dua.', image='tiu-2024-q32.png'),
    row(33, 'Perhatikan gambar pada lampiran soal. Carilah gambar yang sesuai untuk melengkapi analogi gambar berikut.', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 4, 'Gambar pertama dibagi menjadi beberapa bagian sesuai jumlah sisinya untuk membentuk gambar kedua. Prinsip yang sama membuat jawaban yang tepat adalah gambar keempat.', image='tiu-2024-q33.png'),
    row(34, 'Perhatikan gambar pada lampiran soal. Carilah gambar yang sesuai untuk melengkapi analogi gambar berikut.', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 2, 'Pada setiap baris, gambar dicerminkan dari kiri ke kanan lalu ada elemen yang bertambah atau berkurang. Dengan pola itu, jawaban yang sesuai adalah gambar kedua.', image='tiu-2024-q34.png'),
    row(35, 'Perhatikan gambar pada lampiran soal. Carilah gambar yang sesuai untuk melengkapi analogi gambar berikut.', ['Gambar 1', 'Gambar 2', 'Gambar 3', 'Gambar 4', 'Gambar 5'], 1, 'Segitiga pada baris atas dipotong menjadi dua lalu dibalik. Prinsip yang sama diterapkan pada bangun di bawahnya, sehingga pilihan yang tepat adalah gambar pertama.', image='tiu-2024-q35.png'),
]


IMAGE_CROPS = {
    'tiu-2024-q29.png': ('page-55.png', (70, 70, 430, 285)),
    'tiu-2024-q30.png': ('page-56.png', (65, 65, 435, 285)),
    'tiu-2024-q31.png': ('page-57.png', (65, 55, 445, 255)),
    'tiu-2024-q32.png': ('page-58.png', (65, 55, 445, 245)),
    'tiu-2024-q33.png': ('page-59.png', (60, 60, 445, 305)),
    'tiu-2024-q34.png': ('page-60.png', (60, 55, 450, 355)),
    'tiu-2024-q35.png': ('page-61.png', (60, 50, 445, 280)),
}


def export_rows(rows: list[dict[str, object]]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / 'cpns_tiu_2024_final.csv'
    xlsx_path = OUTPUT_DIR / 'cpns_tiu_2024_final.xlsx'

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


def crop_question_images() -> None:
    IMAGE_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, (source_name, box) in IMAGE_CROPS.items():
        image = Image.open(IMAGE_SOURCE_DIR / source_name).convert('RGB')
        cropped = image.crop(box)
        cropped.save(IMAGE_EXPORT_DIR / filename)


def sync_to_database(rows: list[dict[str, object]]) -> None:
    parent_category, _ = Category.objects.get_or_create(
        name='CPNS',
        parent=None,
        defaults={'description': 'Kategori utama soal CPNS.'},
    )
    category, _ = Category.objects.get_or_create(
        name='TIU 2024',
        parent=parent_category,
        defaults={'description': 'Tes Intelegensia Umum CPNS 2024'},
    )
    category.description = 'Tes Intelegensia Umum CPNS 2024'
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
        if item['image']:
            image_path = IMAGE_EXPORT_DIR / str(item['image'])
            with image_path.open('rb') as handle:
                question.image.save(image_path.name, File(handle), save=True)
        else:
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
    crop_question_images()
    csv_path, xlsx_path = export_rows(ROWS)
    sync_to_database(ROWS)
    print(f'Exported CSV: {csv_path}')
    print(f'Exported XLSX: {xlsx_path}')
    print(f'Exported image dir: {IMAGE_EXPORT_DIR}')
    print(f'Synced {len(ROWS)} questions into category CPNS > TIU 2024')


if __name__ == '__main__':
    main()
