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
            upload_file = request.FILES.get('csv_file')
            
            if not upload_file:
                messages.error(request, 'Please upload a CSV or ZIP file.')
                return redirect('..')
            
            is_zip = upload_file.name.lower().endswith('.zip')
            is_csv = upload_file.name.lower().endswith('.csv')
            
            if not (is_zip or is_csv):
                messages.error(request, 'File must be CSV or ZIP.')
                return redirect('..')
            
            try:
                import zipfile
                import os
                from django.core.files import File
                from django.conf import settings
                import shutil
                import tempfile
                
                # Create temp directory
                temp_dir = tempfile.mkdtemp()
                
                csv_path = None
                image_map = {} # Filename -> full path
                
                if is_zip:
                    with zipfile.ZipFile(upload_file, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Find CSV and Images
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.lower().endswith('.csv') and not csv_path:
                                csv_path = os.path.join(root, file)
                            elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                image_map[file] = os.path.join(root, file)
                                
                    if not csv_path:
                        messages.error(request, 'No CSV file found in the ZIP archive.')
                        shutil.rmtree(temp_dir)
                        return redirect('..')
                        
                else:
                    # Save uploaded CSV to temp file
                    csv_path = os.path.join(temp_dir, 'import.csv')
                    with open(csv_path, 'wb+') as destination:
                        for chunk in upload_file.chunks():
                            destination.write(chunk)
                
                # Process CSV
                with open(csv_path, 'r', encoding='utf-8-sig') as f:
                    # Auto-detect delimiter
                    sample = f.read(2048)
                    f.seek(0)
                    first_line = sample.split('\n')[0]
                    delimiter = ';' if first_line.count(';') > first_line.count(',') else ','
                    
                    reader = csv.DictReader(f, delimiter=delimiter)
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]
                    
                    created_count = 0
                    
                    for row in reader:
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
                        
                        try:
                            order_val = int(row.get('order', 0))
                        except ValueError:
                            order_val = 0
                            
                        # Create Question
                        question = Question.objects.create(
                            category=category,
                            text=question_text,
                            order=order_val
                        )
                        
                        # Handle Image
                        image_filename = row.get('image', '')
                        if image_filename and image_filename in image_map:
                            img_path = image_map[image_filename]
                            with open(img_path, 'rb') as img_file:
                                question.image.save(image_filename, File(img_file), save=True)
                        
                        # Choices
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
                
                # Cleanup
                shutil.rmtree(temp_dir)
                messages.success(request, f'Successfully imported {created_count} questions{" with images" if is_zip else ""}! (Delimiter: {delimiter})')
                return redirect('..')
                
            except Exception as e:
                # Ensure cleanup happens
                if 'temp_dir' in locals() and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                messages.error(request, f'Error importing: {str(e)}')
                return redirect('..')
        
        return render(request, 'admin/import_questions.html')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

admin.site.site_header = "Test Soal CPNS & BUMN Administration"
admin.site.site_title = "Test Soal Admin"
admin.site.index_title = "Welcome to Test Soal Admin Panel"
