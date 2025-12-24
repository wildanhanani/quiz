"""
Script to update user subscription package
Usage: python manage.py shell < update_subscription.py
"""

from django.contrib.auth.models import User
from quiz.models import Subscription

print("=" * 50)
print("UPDATE USER SUBSCRIPTION")
print("=" * 50)

# Get username from input
username = input("\nMasukkan username: ")

try:
    user = User.objects.get(username=username)
    subscription = user.subscription
    
    print(f"\nUser: {user.username}")
    print(f"Current Package: {subscription.get_package_display()}")
    print(f"Max Attempts: {subscription.max_attempts_per_quiz}")
    print(f"Max Categories: {subscription.max_categories}")
    
    print("\n" + "=" * 50)
    print("PILIH PAKET BARU:")
    print("=" * 50)
    print("1. FREE - Gratis (1x attempt per quiz, kategori gratis saja)")
    print("2. BASIC - Rp 10.000 (3x attempts, 5 kategori)")
    print("3. PREMIUM - Rp 50.000 (5x attempts, semua kategori)")
    
    choice = input("\nPilihan (1/2/3): ")
    
    if choice == '1':
        subscription.package = 'FREE'
        subscription.max_attempts_per_quiz = 1
        subscription.max_categories = 999
    elif choice == '2':
        subscription.package = 'BASIC'
        subscription.max_attempts_per_quiz = 3
        subscription.max_categories = 5
    elif choice == '3':
        subscription.package = 'PREMIUM'
        subscription.max_attempts_per_quiz = 5
        subscription.max_categories = 999
    else:
        print("❌ Pilihan tidak valid!")
        exit()
    
    subscription.save()
    
    print("\n" + "=" * 50)
    print("✅ SUBSCRIPTION UPDATED!")
    print("=" * 50)
    print(f"User: {user.username}")
    print(f"New Package: {subscription.get_package_display()}")
    print(f"Max Attempts: {subscription.max_attempts_per_quiz}")
    print(f"Max Categories: {subscription.max_categories}")
    print("=" * 50)
    
except User.DoesNotExist:
    print(f"\n❌ User '{username}' tidak ditemukan!")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
