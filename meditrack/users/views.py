from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = form.user
      login(request, user)
      return redirect('dashboard')
  else:
    form = LoginForm()
  return render(request, 'users/login.html', {'form': form})