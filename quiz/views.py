from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Question, Choice, QuizAttempt, Subscription
import json

@login_required
def dashboard(request):
    subscription = request.user.subscription
    categories = Category.objects.all()
    
    # Filter categories based on subscription
    if subscription.package == 'BASIC':
        # Basic can access up to 5 categories
        categories = categories[:5]
    elif subscription.package == 'FREE':
        # Free can only access non-premium categories
        categories = categories.filter(is_premium=False)
    
    user_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')[:10]
    
    context = {
        'categories': categories,
        'user_attempts': user_attempts,
        'subscription': subscription,
    }
    return render(request, 'quiz/dashboard.html', context)

@login_required
def take_quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subscription = request.user.subscription
    
    # Check if user can access this category
    if not subscription.can_access_category(category):
        messages.error(request, 'Anda perlu upgrade paket untuk mengakses kategori ini.')
        return redirect('dashboard')
    
    # Check attempt limit for all packages (including FREE)
    remaining_attempts = subscription.get_remaining_attempts(category)
    if remaining_attempts <= 0:
        messages.error(request, f'Anda sudah mencapai batas maksimal ({subscription.max_attempts_per_quiz}x) untuk kuis ini. Upgrade paket untuk attempt lebih banyak.')
        return redirect('dashboard')
    
    questions = category.questions.all().order_by('order')
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                user_answers[str(question.id)] = {
                    'selected': int(selected_choice_id),
                    'correct': choice.is_correct
                }
                if choice.is_correct:
                    score += 1
        
        # Save Attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            category=category,
            score=score,
            total_questions=total,
            answers=user_answers
        )
        
        return redirect('quiz_result', attempt_id=attempt.id)

    context = {
        'category': category,
        'questions': questions,
        'remaining_attempts': remaining_attempts,
        'subscription': subscription,
    }
    return render(request, 'quiz/take_quiz.html', context)

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    category = attempt.category
    percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
    
    # Get questions with user answers and correct answers
    questions_with_answers = []
    for question in category.questions.all().order_by('order'):
        user_answer_data = attempt.answers.get(str(question.id), {})
        selected_choice_id = user_answer_data.get('selected')
        
        choices_data = []
        for choice in question.choices.all():
            choices_data.append({
                'id': choice.id,
                'text': choice.text,
                'is_correct': choice.is_correct,
                'was_selected': choice.id == selected_choice_id
            })
        
        questions_with_answers.append({
            'question': question,
            'choices': choices_data,
            'user_was_correct': user_answer_data.get('correct', False)
        })
    
    context = {
        'attempt': attempt,
        'category': category,
        'score': attempt.score,
        'total': attempt.total_questions,
        'percentage': percentage,
        'questions_with_answers': questions_with_answers,
    }
    return render(request, 'quiz/result.html', context)

@login_required
def history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
    context = {
        'attempts': attempts
    }
    return render(request, 'quiz/history.html', context)
