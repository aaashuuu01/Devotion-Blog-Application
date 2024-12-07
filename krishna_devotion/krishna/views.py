from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    query = request.GET.get('search', '')  
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.all()  
    return render(request, 'home.html', {'posts': posts, 'query': query}) 

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            messages.success(request, 'Post submitted successfully!')
            return redirect('home')  
        else:
            messages.error(request, 'Error in form submission. Please try again.')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  
    return render(request, 'post_detail.html', {'post': post})  

def blog_page(request):
    latest_posts = Post.objects.order_by('-created_at')[:5]  
    return render(request, 'blog.html', {'latest_posts': latest_posts})

def blog(request):
    return render(request, 'blog.html')  

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)  
        else:
            messages.error(request, 'Error in form submission. Please try again.')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')  
    return render(request, 'confirm_delete.html', {'post': post})

def contact(request):
    return render(request, 'contact.html')  

def about(request):
    return render(request, 'about.html')  
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'User created successfully.')
        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)  
    return redirect('index') 

def index(request):
    return render(request, 'index.html') 

def send_email_to_users(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        users = User.objects.all()
        recipient_list = [user.email for user in users if user.email]  

        if recipient_list:
            send_mail(
                subject,
                message,
                'ashutoshmmu750@gmail.com', 
                recipient_list,
                fail_silently=False,
            )
            messages.success(request, 'Emails sent successfully!')
        else:
            messages.error(request, 'No registered users to send emails to.')

        return redirect('home')  

    return render(request, 'send_email.html')  