from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
        help_text='Kosongkan jika ini adalah kategori utama.',
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_premium = models.BooleanField(default=False, help_text="Kategori premium (butuh paket berbayar)")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['parent__name', 'name', 'id']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        return self.name

    @property
    def effective_is_premium(self):
        return self.is_premium or bool(self.parent and self.parent.is_premium)

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # Changed from CharField to TextField for unlimited length
    explanation = models.TextField(blank=True)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
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
    prefers_timer = models.BooleanField(default=False)
    preferred_timer_minutes = models.PositiveIntegerField(default=20)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def ensure_for_user(cls, user):
        subscription, _ = cls.objects.get_or_create(user=user)
        return subscription
    
    def __str__(self):
        return f"{self.user.username} - {self.get_package_display()}"

    def get_accessible_categories(self):
        categories = Category.objects.exclude(
            parent__isnull=True,
            subcategories__isnull=False,
            questions__isnull=True,
        ).select_related('parent').distinct()

        if self.package == 'PREMIUM':
            return categories
        if self.package == 'BASIC':
            return categories[:self.max_categories]
        return categories.filter(
            is_premium=False,
        ).filter(
            Q(parent__isnull=True) | Q(parent__is_premium=False)
        )
    
    def get_remaining_attempts(self, category):
        """Get remaining attempts for a specific category"""
        attempts_count = QuizAttempt.objects.filter(
            user=self.user,
            category=category
        ).count()
        return max(0, self.max_attempts_per_quiz - attempts_count)
    
    def can_access_category(self, category):
        """Check if user can access this category"""
        if category.parent_id is None and category.subcategories.exists() and not category.questions.exists():
            return False
        if self.package == 'PREMIUM':
            return True
        if self.package == 'BASIC':
            allowed_ids = list(
                self.get_accessible_categories().values_list('id', flat=True)[:self.max_categories]
            )
            return category.id in allowed_ids
        return not category.effective_is_premium

@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.ensure_for_user(instance)

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    answers = models.JSONField(default=dict, blank=True)  # Store user answers
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.full_name} - {self.score}"
    
    @property
    def is_passed(self):
        if self.total_questions == 0:
            return False
        return (self.score / self.total_questions) >= 0.6
    
    class Meta:
        ordering = ['-completed_at']
