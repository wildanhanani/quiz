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

print("\n" + "="*50)
print("✓ Data population complete!")
print("="*50)
print("\nTest Credentials:")
print("Username: testuser")
print("Password: test123")
print("\nAdmin Credentials:")
print("Username: admin")
print("Password: admin")
