from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def index(request):
    return render(request, 'index.html')

def pricing(request):
    return render(request, 'pricing.html')

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
    return render(request, 'registration/register.html', {'form': form})
