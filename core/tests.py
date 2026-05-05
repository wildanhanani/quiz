from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_register_page_renders_without_social_app_configuration(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buat Akun Baru')
        self.assertNotContains(response, 'Atau daftar dengan')
        self.assertNotContains(response, '/accounts/google/login/')

    def test_register_creates_inactive_user_with_subscription(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        self.assertEqual(user.subscription.package, 'FREE')


class HealthCheckTests(TestCase):
    def test_healthz_returns_ok(self):
        response = self.client.get(reverse('healthz'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'database': 'ok'})
        self.assertEqual(response['Cache-Control'], 'no-store')


class OfflinePageTests(TestCase):
    def test_offline_page_renders(self):
        response = self.client.get(reverse('offline'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Koneksi sedang tidak tersedia')
        self.assertContains(response, 'Coba Lagi')


class LoginViewTests(TestCase):
    def test_login_page_renders_without_social_app_configuration(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Masuk ke Akun')
