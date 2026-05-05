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
        'category': 'TWK 2024',
        'category_description': 'Tes Wawasan Kebangsaan CPNS 2024',
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
    row(
        1,
        'Membina persatuan dan kesatuan dihubungkan dengan semboyan Bhinneka Tunggal Ika mengandung makna bahwa ....',
        [
            'Dalam bergaul harus dapat menyesuaikan diri',
            'Kebudayaan daerah harus terus dilestarikan',
            'Dalam pergaulan tidak boleh membedakan suku',
            'Kebudayaan masyarakat tidak tergantikan budaya lain',
            'Keanekaragaman tak mungkin dipersatukan',
        ],
        3,
        'Bhinneka Tunggal Ika menegaskan bahwa bangsa Indonesia tetap satu meskipun berbeda-beda, sehingga dalam pergaulan tidak boleh membedakan suku.',
    ),
    row(
        2,
        'Pak Suyatno adalah orang yang sombong. Ia selalu menilai orang dari kekayaan dan kedudukannya. Sikap Pak Suyatno bertentangan dengan sila ....',
        [
            'Ketuhanan Yang Maha Esa',
            'Kemanusiaan yang adil dan beradab',
            'Persatuan Indonesia',
            'Kerakyatan yang dipimpin oleh hikmat kebijaksanaan dalam permusyawaratan perwakilan',
            'Keadilan bagi seluruh rakyat Indonesia',
        ],
        2,
        'Sifat sombong bertentangan dengan nilai kemanusiaan yang adil dan beradab, karena merendahkan martabat orang lain dan tidak menghargai sesama.',
    ),
    row(
        3,
        'Pembangunan tidak boleh bersifat pragmatis, hal ini berarti ....',
        [
            'Pembangunan tidak hanya mementingkan tindakan nyata dan mengabaikan pertimbangan etis',
            'Pembangunan hanya mengikuti peraturan masing-masing instansi dan mengabaikan manusia nyata',
            'Pembangunan tidak boleh mengorbankan manusia nyata melainkan menghormati harkat dan martabat bangsa',
            'Pembangunan melibatkan masyarakat sebagai tujuan pembangunan dan keputusan yang menyangkut kebutuhan mereka',
            'Pembangunan tidak hanya mementingkan tindakan nyata dan menghapuskan kemiskinan struktural',
        ],
        1,
        'Pembangunan yang sesuai Pancasila tidak boleh pragmatis. Artinya, pembangunan tidak boleh hanya mengejar tindakan nyata sambil mengabaikan pertimbangan etis.',
    ),
    row(
        4,
        'Pembangunan yang dilaksanakan mengacu pada standar nilai Pancasila adalah maksud dari ....',
        [
            'Pancasila sebagai ideologi terbuka',
            'Pancasila sebagai ideologi tertutup',
            'Pancasila sebagai nilai instrumental',
            'Pancasila sebagai dasar negara',
            'Pancasila sebagai paradigma pembangunan',
        ],
        5,
        'Pancasila sebagai paradigma pembangunan berarti nilai-nilai dasarnya menjadi acuan, tolok ukur, dan arah dalam seluruh proses pembangunan nasional.',
    ),
    row(
        5,
        'Berikut ini yang termasuk dimensi realitas sila ke-3 Pancasila, kecuali ....',
        [
            'Menghindari sikap chauvinisme dan primordialisme secara tepat',
            'Memajukan pergaulan demi kemajuan bangsa',
            'Membina hubungan baik dengan semua unsur bangsa',
            'Mengembangkan sikap saling tenggang rasa dan tepa selira',
            'Rela berkorban demi kepentingan bangsa dan negara',
        ],
        4,
        'Yang tidak termasuk dimensi realitas sila ketiga pada soal ini adalah sikap saling tenggang rasa dan tepa selira.',
    ),
    row(
        6,
        'Mengembangkan sikap bahwa bangsa Indonesia merupakan bagian dari seluruh umat manusia merupakan perwujudan sila ....',
        ['Pertama', 'Kedua', 'Ketiga', 'Keempat', 'Kelima'],
        2,
        'Sikap merasa sebagai bagian dari seluruh umat manusia merupakan pengamalan sila kedua, Kemanusiaan yang Adil dan Beradab.',
    ),
    row(
        7,
        'Pancasila sebagai paradigma pembangunan politik harus mampu ....',
        [
            'Menjadikan rakyat sebagai subjek politik bukan objek politik',
            'Menjadi sumber dari segala sumber hukum',
            'Pengontrol atas kekuasaan yang absolut',
            'Pedoman hidup berkebangsaan',
            'Memberi perlindungan hak asasi bagi rakyat',
        ],
        1,
        'Dalam paradigma pembangunan politik, Pancasila mengarahkan agar rakyat menjadi subjek politik, bukan sekadar objek kebijakan.',
    ),
    row(
        8,
        'Menurut pernyataan dalam Pembukaan UUD 1945 perjuangan kemerdekaan merupakan tindakan yang diberikan oleh Allah karena ....',
        [
            'Kehidupan kebangsaan yang bebas merupakan keinginan luhur',
            'Bangsa Indonesia adalah bangsa yang religius',
            'Kemerdekaan itu sudah lama diperjuangkan',
            'Banyak pengorbanan yang harus diberikan untuk mendapatkan kemerdekaan',
            'Kemerdekaan karunia Allah yang tidak perlu diperjuangkan',
        ],
        2,
        'Frasa "Atas berkat rahmat Allah Yang Maha Kuasa" menunjukkan bangsa Indonesia menjunjung nilai ketuhanan, sehingga simpulannya bangsa Indonesia adalah bangsa yang religius.',
    ),
    row(
        9,
        'Salah satu bentuk pengamalan sila ke-4 di bawah ini adalah ....',
        [
            'Kita tidak boleh memaksakan kehendak kita kepada orang lain',
            'Mengembangkan sikap hormat menghormati dan bekerja sama dengan bangsa lain',
            'Menjunjung tinggi hak asasi manusia',
            'Menyadari bahwa kita mempunyai hak dan kewajiban yang sama',
            'Mengembangkan sikap saling mencintai sesama manusia',
        ],
        1,
        'Sila keempat menekankan musyawarah dan kebijaksanaan. Karena itu, kita tidak boleh memaksakan kehendak kepada orang lain.',
    ),
    row(
        10,
        'Rumusan dan susunan Pancasila yang benar dan sah tercantum dalam ....',
        [
            'Pidato Moh. Yamin tanggal 29 Mei 1945',
            'Piagam Jakarta',
            'Pidato Bung Karno tanggal 1 Juni 1945',
            'Pembukaan UUD 1945',
            'Mukadimah Konstitusi Sementara RIS',
        ],
        4,
        'Rumusan dan susunan Pancasila yang sah tercantum dalam Pembukaan UUD 1945 yang disahkan pada 18 Agustus 1945.',
    ),
    row(
        11,
        'Janji kemerdekaan yang akan diberikan Jepang setelah kekalahan Jepang pada saat Perang Dunia II diumumkan oleh ....',
        [
            'Laksamana Maeda',
            'Perdana Menteri Koiso',
            'Ichikawa Taisho',
            'Marsekal Terauchi',
            'Kumakichi Harada',
        ],
        2,
        'Janji kemerdekaan Indonesia diumumkan oleh Perdana Menteri Koiso pada 7 September 1944.',
    ),
    row(
        12,
        'Interaksi masyarakat yang berorientasi ke atas, sangat mementingkan hubungan yang formal dan bersifat impersonal. Gambaran tersebut merupakan etos kebudayaan masyarakat ....',
        ['Elite', 'Birokrat', 'Petani', 'Buruh', 'Tradisional'],
        2,
        'Hubungan yang formal, impersonal, dan berorientasi ke atas merupakan ciri etos kebudayaan masyarakat birokrat.',
    ),
    row(
        13,
        'Berdasarkan UUD 1945, setiap pemberian amnesti dan abolisi, pengangkatan dan penerimaan duta, serta pernyataan perang harus disetujui oleh ....',
        ['Menteri pertahanan', 'Panglima TNI', 'Panglima Polri', 'DPR', 'Menteri Hukum dan HAM'],
        4,
        'Menurut UUD 1945, tindakan seperti pemberian amnesti dan abolisi, pengangkatan duta, serta pernyataan perang harus mendapat persetujuan DPR.',
    ),
    row(
        14,
        'Dalam tata aturan perundang-undangan RI, UUD 1945 menempati posisi tertinggi sedangkan peraturan perundang-undangan yang menempati posisi terbawah adalah ....',
        ['Perpu', 'Perda', 'Perpres', 'Peraturan Pemerintah', 'Hukum adat'],
        2,
        'Dalam hierarki yang digunakan pada sumber soal, urutan terendah adalah Peraturan Daerah setelah UUD, UU/Perpu, PP, dan Perpres.',
    ),
    row(
        15,
        'Negara menghormati dan memelihara bahasa daerah sebagai kekayaan budaya nasional. Hal ini tercantum dari pasal ....',
        ['23', '24', '27', '31', '32'],
        5,
        'Ketentuan bahwa negara menghormati dan memelihara bahasa daerah sebagai kekayaan budaya nasional terdapat dalam Pasal 32.',
    ),
    row(
        16,
        'Mewujudkan nasionalisme yang tinggi dari rakyat Indonesia, yang lebih mengutamakan kepentingan nasional daripada kepentingan golongan merupakan ....',
        [
            'Tujuan ketahanan nasional',
            'Pengertian ketahanan nasional',
            'Tujuan pembangunan nasional',
            'Pengertian wawasan nusantara',
            'Tujuan wawasan nusantara',
        ],
        5,
        'Salah satu tujuan wawasan nusantara adalah membentuk nasionalisme tinggi yang mengutamakan kepentingan nasional di atas kepentingan golongan.',
    ),
    row(
        17,
        'Pak Andri mendapatkan tugas dari kantornya untuk mengikuti pelatihan di luar kota selama tiga hari. Di luar dugaan, pelatihan tersebut selesai lebih cepat dari jadwal yang ditentukan yaitu selama dua hari. Jika Anda menjadi Pak Andri, apa yang akan Anda lakukan ....',
        [
            'Menikmati sisa satu hari untuk berjalan-jalan',
            'Melaporkan ke kantor bahwa kegiatan sudah selesai dalam dua hari, dan menunggu arahan berikutnya',
            'Segera pulang dan memilih berlibur bersama keluarga',
            'Segera pulang dan memilih libur di rumah',
            'Merahasiakan bahwa pelatihan selesai lebih cepat dan memanfaatkan sisa waktu untuk bertemu teman',
        ],
        2,
        'Tindakan yang tepat adalah segera melaporkan kondisi sebenarnya kepada kantor dan menunggu arahan, karena itu menunjukkan integritas dan profesionalitas.',
    ),
    row(
        18,
        'Dalam ketatanegaraan Republik Indonesia, pembentukan sebuah provinsi dapat dilakukan dengan memiliki paling sedikitnya ....',
        [
            '5 (lima) kabupaten/kota',
            '7 (tujuh) kabupaten/kota',
            '10 (sepuluh) kabupaten/kota',
            '1/2 kabupaten/kota dari jumlah provinsi di seluruh Indonesia',
            '2/3 kabupaten/kota dari jumlah provinsi di seluruh Indonesia',
        ],
        1,
        'Syarat fisik pembentukan provinsi pada sumber soal mensyaratkan paling sedikit lima kabupaten/kota untuk pembentukan provinsi baru.',
    ),
    row(
        19,
        'Sumber hukum dari keputusan hakim terdahulu yang dijadikan dasar keputusan oleh hakim-hakim lain dalam memutuskan perkara yang sama disebut ....',
        ['statute', 'custom', 'jurisprudensi', 'treaty', 'doktrin'],
        3,
        'Keputusan hakim terdahulu yang dijadikan dasar bagi putusan hakim lain pada perkara serupa disebut yurisprudensi.',
    ),
    row(
        20,
        'Undang-Undang No.31 Tahun 2002 tentang Partai Politik menyatakan bahwa partai politik perlu diadakan karena ....',
        [
            'Terbukti bahwa dengan adanya partai politik negara menjadi demokrasi',
            'Melalui partai politiklah masyarakat dapat memilih presiden dan wakil presiden',
            'Partai politik merupakan satu-satunya wadah untuk menyalurkan aspirasi',
            'Banyaknya tuntutan masyarakat untuk membentuk partai politik',
            'Merupakan salah satu wujud partisipasi masyarakat dalam mengembangkan demokrasi',
        ],
        5,
        'Partai politik merupakan salah satu wahana partisipasi masyarakat dalam kehidupan demokrasi, sehingga keberadaannya dipandang penting.',
    ),
    row(
        21,
        'Soekarno menyampaikan pidato mengenai dasar negara pada tanggal ....',
        ['29 Mei 1945', '30 Mei 1945', '31 Mei 1945', '1 Juni 1945', '22 Juni 1945'],
        4,
        'Pada sidang BPUPKI pertama, Ir. Soekarno menyampaikan rumusan lima sila dasar negara pada 1 Juni 1945.',
    ),
    row(
        22,
        'Tokoh yang bersama Bung Karno dan Muhammad Yamin ikut melakukan pembicaraan terbatas mengenai semboyan Bhinneka Tunggal Ika pada sidang-sidang BPUPKI adalah ....',
        ['I Gusti Bagus Sugriwa', 'Adam Malik', 'Sultan Hamid II', 'Ahmad Subarjo', 'I Made Bagus'],
        1,
        'Dalam sumber soal, pembicaraan terbatas mengenai semboyan Bhinneka Tunggal Ika melibatkan Muhammad Yamin, Bung Karno, dan I Gusti Bagus Sugriwa.',
    ),
    row(
        23,
        'Fenomena generasi muda yang mengalami kepudaran terhadap jiwa nasionalisme disebabkan karena ....',
        [
            'Orientasi nasionalisme adalah sikap dan perbuatan',
            'Labeling yang menjadi stigma bagi generasi muda',
            'Ukuran nasionalisme dipahami hanya sebatas perjuangan secara fisik',
            'Kurangnya daya juang terhadap tantangan perubahan zaman',
            'Kurangnya sosok heroisme bagi kaum muda',
        ],
        3,
        'Pada sumber ini, penyebab yang ditekankan adalah pemahaman nasionalisme yang terlalu sempit, seolah hanya berbentuk perjuangan fisik.',
    ),
    row(
        24,
        'Arga meminta uang kepada orangtuanya untuk dibelikan sebuah motor, namun karena orangtuanya hanya bekerja serabutan tidak bisa menuruti keinginannya. Karena menerima penolakan akhirnya Arga kesal dan marah bersama temannya pergi ke joks musik dan melihat sebuah motor. Awalnya Arga tidak ingin mencuri, karena keinginan hatinya berubah dia ingin mencuri motor tersebut. Salah seorang warga melihat hal tersebut lalu meneriakinya maling dan melaporkan Arga ke pihak yang berwajib. Sikap warga menunjukkan ....',
        ['Integritas', 'Profesionalisme', 'Solidaritas', 'Tenggang rasa', 'Rela berkorban'],
        2,
        'Warga yang melaporkan Arga kepada pihak berwajib menunjukkan sikap profesional karena tidak main hakim sendiri dan bertindak sesuai aturan.',
    ),
    row(
        25,
        'Perjanjian bilateral dan multilateral memiliki beberapa perbedaan, salah satunya adalah ....',
        ['Objeknya', 'Sifat instrumennya', 'Strukturnya', 'Cara berlakunya', 'Jumlah pesertanya'],
        5,
        'Perbedaan yang paling jelas antara perjanjian bilateral dan multilateral adalah jumlah pihak atau peserta yang menyepakatinya.',
    ),
    row(
        26,
        'Kebijakan pemotongan nilai uang (sanering) yaitu memotong semua uang yang bernilai Rp2,50 ke atas hingga nilai tinggal setengahnya terjadi pada saat Menteri Keuangan dijabat oleh ....',
        ['Wolopo', 'Ali Sastroamidjojo', 'Burhanudin Harahap', 'Syafruddin Prawiranegara', 'Sri Sultan Hamengkubuwono IX'],
        4,
        'Kebijakan sanering atau Gunting Syafruddin dilakukan saat Menteri Keuangan dijabat oleh Syafruddin Prawiranegara.',
    ),
    row(
        27,
        'Dalam ketatanegaraan Republik Indonesia, pembentukan sebuah dugaan kasus penyebaran hoax dan provokasi melalui media sosial dari kelompok The Family Muslim Cyber Army (MCA). Kelima tersangka ditangkap di daerah berbeda, yakni di Tanjung Priok (Jakarta Utara), Pangkal Pinang, Bali, Sumedang, dan Palu. Berdasarkan barang bukti yang diperoleh polisi, kelompok MCA menyebarkan isu provokatif dan kabar bohong terkait isu suku, agama, ras, dan antargolongan (SARA) melalui jaringan komunikasi WhatsApp. Penyimpangan ini merupakan bentuk pelanggaran sila Pancasila ke ....',
        ['(1)', '(2)', '(3)', '(4)', '(5)'],
        3,
        'Kasus provokasi dan penyebaran isu SARA tersebut dinilai melanggar sila ketiga, Persatuan Indonesia, karena berpotensi memecah belah bangsa.',
    ),
    row(
        28,
        'Isu pemecah belah negara yang dilakukan oleh pihak-pihak tidak bertanggung jawab agar membuat negara menjadi kacau marak terjadi. Sikap kita sebagai warga negara yang baik yaitu ....',
        [
            'Ikut menyebarkan dan memprovokasi',
            'Tidak mudah terimbas isu hoax atau belum tentu kebenarannya',
            'Berpegang teguh pada kepercayaan masing-masing',
            'Waspada dan ikut curiga',
            'Menindaklanjuti kekacauan yang terjadi',
        ],
        2,
        'Sikap yang tepat adalah waspada dan tidak mudah terpengaruh hoax atau informasi yang belum jelas kebenarannya.',
    ),
    row(
        29,
        'Ledakan bom di Poltabes Medan Sumatera Utara pada bulan November lalu, merupakan bentuk penyimpangan dari sila ke ....',
        ['(1)', '(2)', '(3)', '(4)', '(5)'],
        2,
        'Aksi teror yang merendahkan martabat dan keselamatan manusia dipandang sebagai penyimpangan terhadap sila kedua, Kemanusiaan yang Adil dan Beradab.',
    ),
    row(
        30,
        'Pengeboman Surabaya 2018 adalah rangkaian peristiwa meledaknya bom di berbagai tempat di Surabaya dan Sidoarjo, Jawa Timur. Peristiwa ini mengakibatkan korban jiwa dan merupakan contoh kasus bentuk penyimpangan terhadap sila ke ....',
        ['(1)', '(2)', '(3)', '(4)', '(5)'],
        1,
        'Sumber penjelasan pada halaman ini menegaskan bahwa kasus tersebut dikaitkan dengan isu agama dan kebebasan beragama, sehingga substansinya diarahkan pada penyimpangan terhadap sila pertama.',
    ),
]


def export_rows(rows: list[dict[str, object]]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / 'cpns_twk_2024_final.csv'
    xlsx_path = OUTPUT_DIR / 'cpns_twk_2024_final.xlsx'

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
        name='TWK 2024',
        parent=parent_category,
        defaults={'description': 'Tes Wawasan Kebangsaan CPNS 2024'},
    )
    category.description = 'Tes Wawasan Kebangsaan CPNS 2024'
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
    print(f'Synced {len(ROWS)} questions into category CPNS > TWK 2024')


if __name__ == '__main__':
    main()
