from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_premium = models.BooleanField(default=False, help_text="Kategori premium (butuh paket berbayar)")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # Changed from CharField to TextField for unlimited length
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:100]  # Show first 100 chars in admin

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)  # Increased from 200 to 500
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]  # Show first 50 chars

class Subscription(models.Model):
    PACKAGE_CHOICES = [
        ('FREE', 'Gratis'),
        ('BASIC', 'Paket Basic - Rp 10.000'),
        ('PREMIUM', 'Paket Premium - Rp 50.000'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default='FREE')
    max_attempts_per_quiz = models.IntegerField(default=1)  # Changed from 999 to 1
    max_categories = models.IntegerField(default=999)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_package_display()}"
    
    def get_remaining_attempts(self, category):
        """Get remaining attempts for a specific category"""
        attempts_count = QuizAttempt.objects.filter(
            user=self.user,
            category=category
        ).count()
        return max(0, self.max_attempts_per_quiz - attempts_count)
    
    def can_access_category(self, category):
        """Check if user can access this category"""
        if self.package == 'PREMIUM':
            return True
        elif self.package == 'BASIC':
            # Basic can access up to 5 categories
            return True  # We'll check count in view
        else:
            # Free can access non-premium categories
            return not category.is_premium

@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance)

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    answers = models.JSONField(default=dict, blank=True)  # Store user answers
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.score}"
    
    class Meta:
        ordering = ['-completed_at']
