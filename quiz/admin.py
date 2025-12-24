from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .models import Category, Question, Choice, QuizAttempt, Subscription
import csv
import io

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5  # Changed from 4 to 5

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'category', 'order')
    list_filter = ('category',)
    ordering = ('category', 'order')

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score', 'total_questions', 'completed_at')
    list_filter = ('category', 'user', 'completed_at')
    readonly_fields = ('user', 'category', 'score', 'total_questions', 'completed_at', 'answers')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'max_attempts_per_quiz', 'max_categories', 'expires_at')
    list_filter = ('package',)
    search_fields = ('user__username',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_premium', 'question_count')
    list_filter = ('is_premium',)
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Total Questions'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-questions/', self.admin_site.admin_view(self.import_questions), name='import_questions'),
        ]
        return custom_urls + urls
    
    def import_questions(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            
            if not csv_file:
                messages.error(request, 'Please upload a CSV file.')
                return redirect('..')
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be a CSV.')
                return redirect('..')
            
            try:
                # Use utf-8-sig to handle BOM from Excel
                data_set = csv_file.read().decode('utf-8-sig')
                io_string = io.StringIO(data_set)
                
                # Auto-detect delimiter (comma or semicolon)
                sample = io_string.read(2048)
                io_string.seek(0)
                
                # Count occurrences of delimiters in first line
                first_line = sample.split('\n')[0]
                comma_count = first_line.count(',')
                semicolon_count = first_line.count(';')
                
                # Choose delimiter based on which appears more
                delimiter = ';' if semicolon_count > comma_count else ','
                
                reader = csv.DictReader(io_string, delimiter=delimiter)
                
                # Normalize headers (strip whitespace and handle potential BOM issues manually if utf-8-sig failed)
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                
                created_count = 0
                for row in reader:
                    # Strip whitespace from values
                    row = {k: v.strip() if v else '' for k, v in row.items()}
                    
                    category_name = row.get('category', '')
                    if not category_name:
                        continue
                    
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'description': row.get('category_description', '')}
                    )
                    
                    question_text = row.get('question', '')
                    if not question_text:
                        continue
                    
                    # Handle order safely
                    try:
                        order_val = int(row.get('order', 0))
                    except ValueError:
                        order_val = 0
                        
                    question = Question.objects.create(
                        category=category,
                        text=question_text,
                        order=order_val
                    )
                    
                    # Support up to 5 choices (choice_5 is optional)
                    correct_answer_str = row.get('correct_answer', '')
                    
                    for i in range(1, 6):
                        choice_key = f'choice_{i}'
                        choice_text = row.get(choice_key, '')
                        
                        if choice_text:
                            is_correct = correct_answer_str == str(i)
                            Choice.objects.create(
                                question=question,
                                text=choice_text,
                                is_correct=is_correct
                            )
                    
                    created_count += 1
                
                messages.success(request, f'Successfully imported {created_count} questions! (Delimiter: {delimiter})')
                return redirect('..')
                
            except Exception as e:
                messages.error(request, f'Error importing CSV: {str(e)}')
                return redirect('..')
        
        return render(request, 'admin/import_questions.html')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

admin.site.site_header = "Test Soal CPNS & BUMN Administration"
admin.site.site_title = "Test Soal Admin"
admin.site.index_title = "Welcome to Test Soal Admin Panel"
