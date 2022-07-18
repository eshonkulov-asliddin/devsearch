from django.shortcuts import render, redirect
from .models import Profile, Message

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
# from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage




# Create your views here.
def loginUser(request):
    
    page = 'login'

    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist...")   

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user) 
            messages.success(request,'You are logged in')
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-account')  
        else:
            messages.error(request,'Username OR Password is Incorrect')    


    return render(request, 'users/login_registration.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out!') 
    return redirect('login')


def registerUser(request):

    page = 'register'
    form = CustomUserCreationForm()

    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User was created!' )

            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(request, 'An error has occurred during registration...')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_registration.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    profiles, custom_range = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    user = Profile.objects.get(id=pk)

    topSkills = user.skill_set.exclude(description__exact="")
    otherSkills = user.skill_set.filter(description="")
    context = {'user': user, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)    

@login_required(login_url='login')
def userAccount(request):
    user = request.user.profile
    skills = user.skill_set.all()
    projects = user.project_set.all()
    context = {'user': user, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)    

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')
    context = {'form': form}
    return render(request, 'users/edit_form.html', context)    

@login_required(login_url='login')
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            return redirect('user-account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def editSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)    

@login_required(login_url='login')
def deleteSkill(request, pk):
    # I have used dynamic url, but instead i can also use page which helps me to identify the views in delete html
    # page = 'delete'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk) 

    if request.method == 'POST':
        skill.delete() 
        messages.success(request, 'Skill successfully deleted' )  
        return redirect('user-account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)        

@login_required(login_url='login')
def inboxMessages(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount  = messageRequests.filter(is_read=False).count()
    context = {'messages': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    messageObj = Message.objects.get(id=pk)
    if messageObj.is_read == False:
        messageObj.is_read = True
        messageObj.save()
    context = {'messageObj': messageObj}
    return render(request, 'users/message.html', context)    

def sendMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    try:
        sender = request.user.profile
    except:
        sender = None        

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was sent successfully.')

            return redirect('user-profile', pk=recipient.id)
    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/send-message_form.html', context)    