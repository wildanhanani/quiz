from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Question, Choice, QuizAttempt, Subscription


def calculate_percentage(score, total_questions):
    if total_questions <= 0:
        return 0.0
    return round((score / total_questions) * 100, 1)


def build_user_quiz_analytics(user):
    attempts = list(
        QuizAttempt.objects.filter(user=user)
        .select_related('category__parent')
        .order_by('-completed_at', '-id')
    )
    category_stats = {}

    for attempt in attempts:
        percentage = calculate_percentage(attempt.score, attempt.total_questions)
        stats = category_stats.setdefault(
            attempt.category_id,
            {
                'category': attempt.category,
                'attempts_count': 0,
                'percentages': [],
                'latest_percentage': None,
                'latest_completed_at': attempt.completed_at,
                'best_percentage': 0.0,
            },
        )
        stats['attempts_count'] += 1
        stats['percentages'].append(percentage)
        if stats['latest_percentage'] is None:
            stats['latest_percentage'] = percentage
            stats['latest_completed_at'] = attempt.completed_at
        stats['best_percentage'] = max(stats['best_percentage'], percentage)

    category_analytics = []
    for stats in category_stats.values():
        average_percentage = round(
            sum(stats['percentages']) / len(stats['percentages']),
            1,
        )
        trend_percentage = None
        if len(stats['percentages']) >= 2:
            trend_percentage = round(
                stats['percentages'][0] - stats['percentages'][1],
                1,
            )

        category_analytics.append(
            {
                'category': stats['category'],
                'attempts_count': stats['attempts_count'],
                'latest_percentage': stats['latest_percentage'],
                'average_percentage': average_percentage,
                'best_percentage': stats['best_percentage'],
                'trend_percentage': trend_percentage,
                'latest_completed_at': stats['latest_completed_at'],
            }
        )

    category_analytics.sort(
        key=lambda item: (
            -item['latest_percentage'],
            -item['attempts_count'],
            item['category'].name.lower(),
        )
    )

    overall_average = round(
        sum(calculate_percentage(attempt.score, attempt.total_questions) for attempt in attempts) / len(attempts),
        1,
    ) if attempts else 0.0
    strongest_category = category_analytics[0]['category'] if category_analytics else None

    return {
        'total_attempts': len(attempts),
        'categories_completed': len(category_analytics),
        'average_percentage': overall_average,
        'strongest_category': strongest_category,
        'category_analytics': category_analytics,
    }


def group_categories_for_dashboard(categories):
    grouped = {}
    ungrouped = []

    for category in categories:
        if category.parent_id:
            group = grouped.setdefault(
                category.parent_id,
                {
                    'parent': category.parent,
                    'subcategories': [],
                },
            )
            group['subcategories'].append(category)
        else:
            ungrouped.append(category)

    grouped_categories = sorted(
        grouped.values(),
        key=lambda item: item['parent'].name.lower(),
    )
    ungrouped.sort(key=lambda category: category.name.lower())
    return grouped_categories, ungrouped


def get_user_subscription(user):
    return Subscription.ensure_for_user(user)


@login_required
def dashboard(request):
    subscription = get_user_subscription(request.user)
    categories = subscription.get_accessible_categories()
    analytics = build_user_quiz_analytics(request.user)

    for category in categories:
        category.remaining_attempts = subscription.get_remaining_attempts(category)
    grouped_categories, ungrouped_categories = group_categories_for_dashboard(categories)
    
    user_attempts = (
        QuizAttempt.objects.filter(user=request.user)
        .select_related('category__parent')
        .order_by('-completed_at')[:10]
    )
    
    context = {
        'grouped_categories': grouped_categories,
        'ungrouped_categories': ungrouped_categories,
        'user_attempts': user_attempts,
        'subscription': subscription,
        'analytics': analytics,
    }
    return render(request, 'quiz/dashboard.html', context)

@login_required
def take_quiz(request, category_id):
    category = get_object_or_404(Category.objects.select_related('parent'), id=category_id)
    subscription = get_user_subscription(request.user)
    
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
    total_questions = questions.count()
    auto_timer_minutes = max(1, min(total_questions, 180))
    
    if request.method == 'POST':
        score = 0
        total = total_questions

        user_answers = {
            '_meta': {
                'timer_enabled': True,
                'timer_minutes': auto_timer_minutes,
            }
        }
        
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = question.choices.filter(id=selected_choice_id).first()
                if not choice:
                    continue
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
        'auto_timer_minutes': auto_timer_minutes,
        'remaining_attempts': remaining_attempts,
        'subscription': subscription,
    }
    return render(request, 'quiz/take_quiz.html', context)

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related('category__parent'),
        id=attempt_id,
        user=request.user,
    )
    category = attempt.category
    percentage = calculate_percentage(attempt.score, attempt.total_questions)
    category_attempts = QuizAttempt.objects.filter(
        user=request.user,
        category=category,
    ).order_by('-completed_at', '-id')
    category_percentages = [
        calculate_percentage(item.score, item.total_questions)
        for item in category_attempts
    ]
    personal_best = max(category_percentages, default=percentage)
    attempt_number = category_attempts.count()
    attempt_meta = attempt.answers.get('_meta', {})
    remaining_attempts = get_user_subscription(request.user).get_remaining_attempts(category)
    
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
        'personal_best': personal_best,
        'attempt_number': attempt_number,
        'timer_enabled': attempt_meta.get('timer_enabled', False),
        'timer_minutes': attempt_meta.get('timer_minutes'),
        'remaining_attempts': remaining_attempts,
        'questions_with_answers': questions_with_answers,
    }
    return render(request, 'quiz/result.html', context)

@login_required
def history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('category__parent').order_by('-completed_at')
    context = {
        'attempts': attempts
    }
    return render(request, 'quiz/history.html', context)
