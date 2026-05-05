from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.db import connections
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def index(request):
    return render(request, 'index.html')

def pricing(request):
    return render(request, 'pricing.html')


def offline(request):
    return render(request, 'offline.html', status=200)


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_login_enabled'] = SocialApp.objects.filter(
            provider='google',
            sites__id=settings.SITE_ID,
        ).exists()
        return context


def healthz(request):
    try:
        connections['default'].ensure_connection()
    except Exception as exc:
        response = JsonResponse(
            {'status': 'error', 'database': 'unavailable', 'detail': str(exc)},
            status=503,
        )
        response['Cache-Control'] = 'no-store'
        return response

    response = JsonResponse({'status': 'ok', 'database': 'ok'})
    response['Cache-Control'] = 'no-store'
    return response

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Pending Admin Approval
            user.save()
            messages.success(request, 'Account created! Please wait for admin approval before logging in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    google_login_enabled = SocialApp.objects.filter(
        provider='google',
        sites__id=settings.SITE_ID,
    ).exists()
    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'google_login_enabled': google_login_enabled,
        },
    )
