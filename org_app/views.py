from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/organization')
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if  users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                request.session['greeting'] = user.first_name
                return redirect('/organization')
        messages.error(request, "Email for password are not right")
    return redirect('/')

def show_all(request):

    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_organizations': Organization.objects.annotate(likes=Count('favorited_by')).order_by('likes'),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'organization.html', context)

def create_organization(request):
    errors = Organization.objects.organization_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/organization')
    else:
        user = User.objects.get(id=request.session["user_id"])
        organization = Organization.objects.create(
            name = request.POST['name'],
            description = request.POST['description'],
            creator = user
        )
        messages.success(request, "Organization created")
        organization.favorited_by.add(User.objects.get(id=request.session['user_id']))
        return redirect(f'/organization')

def one_org(request, id):
    context = {
        'one_org': Organization.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "one_org.html", context)


def delete(request, id):
        organization= Organization.objects.get(id=id)
        organization.delete()
        return redirect("/organization")


def join_org(request, id):
    user = User.objects.get(id=request.session['user_id'])
    org= Organization.objects.get(id=id)
    org.favorited_by.add(user)
    return redirect(f'/organization/{id}')

def leave_org(request, id):
    user = User.objects.get(id=request.session['user_id'])
    org= Organization.objects.get(id=id)
    org.favorited_by.remove(user)
    return redirect(f'/organization/{id}')

def logout(request):
    request.session.flush()

    return redirect('/')