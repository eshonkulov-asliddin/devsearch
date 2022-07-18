from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Project, Tag, Review
from .forms import ProjectForm, ReviewForm
from django.contrib import messages 
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.contrib.auth.decorators import login_required




# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    projects, custom_range = paginateProjects(request, projects, 3)        

    context = {'projects':projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review submitted successfully')
        return redirect('project' , pk=projectObj.id)

    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def CreateProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            newtags = request.POST.get('newtags').replace(",", " ").split()
            project = form.save(commit=False)
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            project.owner = profile
            project.save()
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)                


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(",", " ").split()
        # print('DATA:', newtags)

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('user-account')
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)     

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project successfully deleted')  

        return redirect('user-account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)    