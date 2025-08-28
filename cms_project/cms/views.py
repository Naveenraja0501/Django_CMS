from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Article

# --- Authentication Views ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            return redirect('article_list')
    else:
        form = UserCreationForm()
    return render(request, 'cms/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'cms/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

# --- Article Views (Protected) ---
@login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'cms/article_list.html', {'articles': articles})

@login_required
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'cms/article_detail.html', {'article': article})
