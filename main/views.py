from django.shortcuts import render
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpForm, NewProjectForm, VoteForm
from .models import Profile, Project, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def welcome(request):
    return render(request, 'welcome.html')

@login_required(login_url='/accounts/login/')
def home(request):
    project= Project.all_projects()
    json_projects = []
    for project in project:

        pic = Profile.objects.filter(user=project.user.id).first()
        if pic:
            pic = pic.profile_pic
        else:
            pic =''
        obj = dict(
            title=project.title,
            image=project.image,
            link=project.link,
            description=project.description,
            avatar=pic,
            author=project.user.username,

        )
        json_projects.append(obj)
        # print(json_projects)
    
    return render(request, 'all-main/home.html', {"json_projects": json_projects})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form, 'user':user})

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'all-main/profile.html', context)


@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('home')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)

        context = {
            'user_form': user_form,
            'profile_form': profile_form

        }

    return render(request, 'all-main/update_profile.html', context)

@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
   
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
           
            image.save()
            
    else:
        form = NewProjectForm()
    return render(request, 'all-main/new_project.html', {"form": form})


def search_results(request):
    if 'project' in request.GET and request.GET['project']:
        search_term =request.GET.get('project')
        searched_project = Project.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{"message":message,"projects":searched_project})

    else:
        message = "You haven't searched for any term"

        return render(request,'all-main/search.html',{'message':message})

@login_required(login_url='/accounts/login/')
def rating(request,id):
    
    project=Project.objects.get(id=id)
    rating=round(((project.design + project.usability + project.content)/3),1)
    if request.method == 'POST':
        form=VoteForm(request.POST)
        if form.is_valid:
            project.vote+=1
            if project.design ==0:
                project.design = int(request.POST['design'])

            else:
                project.design = (project.design + int(request.POST['design']))/2

            if project.usability == 0:
                project.usability = int(request.POST['usability'])
            else:
                project.usability = (project.design + int(request.POST['usability']))/2
            if project.content == 0:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2
            project.save()
            return redirect('new_project')
    else:
        form = VoteForm()
    return render(request,'all-main/rating.html',{'form':form,'project':project,'rating':rating})   

@login_required(login_url='/accounts/login/')
def comment(request, project_id):
    current_user = request.user
    project = Project.objects.get(id=project_id)
    profile = Profile.objects.filter(user=current_user.id).first()
    if request.method == 'POST':
        form=NewCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.project=project
            comment.save()
            
            return redirect('new_project')

    else:
        form = NewCommentForm()

    return render(request, 'all-main/comment.html', {'form': form,'profile':profile, 'project':project, 'project_id':project_id})