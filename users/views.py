from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as log
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from blog.models import Post,Comment
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import *
from .models import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been successfully created')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            
            log(request, new_user)
            return render(request, 'users/profile_complete.html')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    form = UserCreationForm()
    return render(request, 'users/login.html', {'form': form})



def after_login(request):
    try:
        if request.user.authority.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    try:
        if request.user.anonymous.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    try:
        if request.user.journalist.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    return redirect('profile_page')  # profile complete page

def profile_page(request):
    if request.method == 'POST':
        role = request.POST.get('profile', '')
        if (role == "authority"):
            current_site = get_current_site(request)
            mail = request.POST['email']
            deptid = request.POST['dept_id']
            deptname = request.POST['dept_name']
            print(deptid, deptname)
            authority = Authority()
            authority.user = User.objects.get(username=request.user)
            authority.Email_id = mail
            authority.Dept_id = deptid
            authority.Dept_name = deptname
            user = authority.user
            user.save()
            authority.save()
            print(mail)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'shadowiiits2@gmail.com', [mail])
            return render(request, 'email_confirmation.html')

        elif (role == "journalist"):
            current_site = get_current_site(request)
            mail = request.POST['email']
            companyid = request.POST['company_id']
            companyname = request.POST['company_name']
            journalist = Journalist()
            journalist.user = User.objects.get(username=request.user)
            journalist.Email_id = mail
            journalist.Dept_id = companyid
            journalist.Dept_name = companyname
            user = journalist.user
            user.save()
            journalist.save()
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'shadowiiits2@gmail.com', [mail])
            return render(request, 'email_confirmation.html')
        else:
            anonymus = Anonymous()
            anonymus.user = request.user
            anonymus.profile_complete = True
            anonymus.save()
            return redirect('blog-home')
    return render(request, 'users/profile_complete.html', )


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        authority_items = Authority.objects.filter(user=user)
        if len(authority_items) != 0:
            authority = Authority.objects.get(user=user)
            authority.profile_complete = True
            print(authority.Email_id)
            authority.save()
            log(request, user)
            return redirect('blog-home')
        journalist_items = Journalist.objects.filter(user=user)
        if len(journalist_items) != 0:
            journalist = Journalist.objects.get(user=user)
            journalist.profile_complete = True
            journalist.save()
            log(request, user)
            return redirect('blog-home')

    else:
        return HttpResponse('Activation link is invalid!')




@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)

    user_posts = Post.objects.filter(
        author=request.user).order_by('-date_posted')

    flag = []
    try:
        querry = Authority.objects.get(user=user)
    except:
        flag += [1]

    try:
        querry = Journalist.objects.get(user=user)
    except:
        flag += [2]

    try:
        querry = Anonymous.objects.get(user=user)
    except:
        flag += [3]

    if 1 not in flag:
        # querry = Authority.objects.get(user=user)
        context = {
            'p_form': ProfileUpdateForm,
            'user_posts': user_posts,
            'flag': flag,


        }
    if 2 not in flag:
        # querry = Journalist.objects.get(user=user)
        context = {
            'p_form': ProfileUpdateForm,
            'user_posts': user_posts,
            'flag': flag,

        }

    else:
        # querry = Anonymous.objects.get(user=user)
        context = {
            'p_form': ProfileUpdateForm,
            'user_posts': user_posts,
            'flag': flag,

        }

    context = {
        'p_form': ProfileUpdateForm,
        'user_posts': user_posts,
        'flag': flag,
        'email': querry.Email_id,
        'Dept_id': querry.Dept_id,
        'Dept_name': querry.Dept_name,
        'credits':querry.credits,


    }
    return render(request, 'users/profile.html', context)
# Create your views here.


@login_required
def userprofile1(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = comment.author
    p_form = ProfileUpdateForm(request.POST)
    user_posts = Post.objects.filter(
        author=user).order_by('-date_posted')
    flag = []
    try:
        querry = Authority.objects.get(user=user)
    except:
        flag += [1]

    try:
        querry = Journalist.objects.get(user=user)
    except:
        flag += [2]

    try:
        querry = Anonymous.objects.get(user=user)
    except:
        flag += [3]

    if 1 not in flag:
        # querry = Authority.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,

        }
    if 2 not in flag:
        # querry = Journalist.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,

        }

    else:
        # querry = Anonymous.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,

        }

    context = {
        'p_form': p_form,
        'user_posts': user_posts,
        'flag': flag,
        'email': querry.Email_id,
        'Dept_id': querry.Dept_id,
        'Dept_name': querry.Dept_name,
        'author': user,
        'credits' :credits,



    }
    return render(request, 'users/profile1.html', context)


@login_required
def userprofile(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = post.author
    p_form = ProfileUpdateForm(request.POST)
    user_posts = Post.objects.filter(
        author=user).order_by('-date_posted')
    flag = []
    try:
        querry = Authority.objects.get(user=user)
    except:
        flag += [1]

    try:
        querry = Journalist.objects.get(user=user)
    except:
        flag += [2]

    try:
        querry = Anonymous.objects.get(user=user)
    except:
        flag += [3]

    if 1 not in flag:
        # querry = Authority.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,

        }
    if 2 not in flag:
        # querry = Journalist.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,

        }

    else:
        # querry = Anonymous.objects.get(user=user)
        context = {
            'p_form': p_form,
            'user_posts': user_posts,
            'flag': flag,
            'author': user,
            

        }

    context = {
        'p_form': p_form,
        'user_posts': user_posts,
        'flag': flag,
        'email': querry.Email_id,
        'Dept_id': querry.Dept_id,
        'Dept_name': querry.Dept_name,
        'credits' : querry.credits,
        'author': user,


    }
    
    return render(request, 'users/profile1.html', context)


