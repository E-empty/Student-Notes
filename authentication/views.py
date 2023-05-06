import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from studnot.settings import MEDIA_ROOT
from .forms import AddUserForm, NoteForm
from .models import MyGroup, Note, Category, User
from django.core.files.storage import FileSystemStorage
from .forms import GroupForm


@login_required
def group_list(request):
    groups = request.user.groups.all()
    return render(request, 'authentication/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(MyGroup, pk=pk)
    users = User.objects.filter(groups=group)
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')
    if selected_category:
        notes = Note.objects.filter(groups=group, category=selected_category)
    else:
        notes = Note.objects.filter(groups=group)
    add_user_form = AddUserForm(group_id=pk, data=request.POST or None)
    if request.method == 'POST' and add_user_form.is_valid():
        add_user_form.save()
        messages.success(request, 'Użytkownik został dodany do grupy.')
        return redirect('group_detail', pk=pk)
    return render(request, 'authentication/group_detail.html', {'group': group, 'users': users, 'notes': notes, 'add_user_form': add_user_form, 'categories': categories, 'selected_category': selected_category})

@login_required
def group_create(request):
    myuser=request.user
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            if MyGroup.objects.filter(name=group.name).exists():
                messages.error(request, 'Grupa o takiej nazwie już istnieje.')
                return redirect('group_create')
            group.save()
            myuser.groups.add(group)
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'authentication/group_create.html', {'form': form})
#@login_required
#def add_user_to_group(request, group_id):
    group = get_object_or_404(MyGroup, id=group_id)
    if request.user in user.groups.all() and request.user != group.admin:
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                user.groups.add(user)
                messages.success(request, 'Użytkownik został dodany do grupy.')
            return redirect('group_detail', group_id=group.id)
    return render(request, 'authentication/add_user.html')

@login_required
def group_update(request, pk):
    group = get_object_or_404(MyGroup, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            name = form.cleaned_data['name']
            if MyGroup.objects.filter(name=name).exclude(pk=group.pk).exists():
                messages.error(request, 'Grupa o takiej nazwie już istnieje.')
            else:
                group = form.save()
                return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'authentication/group_update.html', {'form': form})

@login_required
def group_delete(request, pk):
    group = get_object_or_404(MyGroup, pk=pk)

    if request.method == 'POST':
        group.delete()
        return redirect('group_list')

    return render(request, 'authentication/group_delete.html', {'group': group})
    
def remove_user_from_group(request, group_id, user_id):
    group = get_object_or_404(MyGroup, id=group_id)
    user = get_object_or_404(User, id=user_id)
    if request.user == group.owner:
        user.groups.remove(group)
    return redirect('group_detail', group_id)

def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        
        
        if User.objects.filter(username=username).exists():
                messages.error(request, "Nazwa użytkownika jest już zajęta.")
                data = {
                'fname': fname,
                'lname': lname,
                'email': email,
            }
                return render(request, "authentication/signup.html", {'data': data})
            
        if User.objects.filter(email=email).exists():
                messages.error(request, "Adres e-mail jest już zarejestrowany.")
                data = {
                'username': username,
                'fname': fname,
                'lname': lname,
                
            }
                return render(request, "authentication/signup.html", {'data': data})
            
        if len(username)>20:
                messages.error(request, "Nazwa użytkownika musi zawierać poniżej 20 znaków!!")
                data = {
                'fname': fname,
                'lname': lname,
                'email': email,
            }
                return render(request, "authentication/signup.html", {'data': data})
            
            
        if pass1 != pass2:
            messages.error(request, "Hasło nie są identyczne!!")
            data = {
                'username': username,
                'fname': fname,
                'lname': lname,
                'email': email,
            }
            return render(request, "authentication/signup.html", {'data': data})

            
        if not username.isalnum():
            messages.error(request, "Nazwa użytkownika może zawierać tylko znaki alfanumeryczne!!")
            data = {
                'fname': fname,
                'lname': lname,
                'email': email,
            }
            return render(request, "authentication/signup.html", {'data': data})
        
        if not fname.isalpha():
            messages.error(request, "Imię i nazwisko może zawierać tylko litery!")
            data = {
                'username': username,
                'email': email,
            }
            return render(request, "authentication/signup.html", {'data': data})
    
        if not lname.isalpha():
            messages.error(request, "Imię i nazwisko może zawierać tylko litery!")
            data = {
                'username': username,
                'email': email,
            }
            return render(request, "authentication/signup.html", {'data': data})
        
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Twoje konto zostało poprawnie założone")
        group = MyGroup.objects.create(name=username, owner=myuser)
        myuser.groups.add(group)
        return redirect('signin')

    return render(request, "authentication/signup.html")
            
            
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        
        if user is not None and user.check_password(pass1):
            login(request, user)
            username = user.username
            messages.success(request, "Zalogowano poprawnie")
            return render(request, "authentication/index.html",{"username":username})
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect('signin')
    
    return render(request, "authentication/signin.html")

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Zostałeś poprawnie wylogowany")
    return redirect('home')
    

@login_required
def create_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            if 'picture' in request.FILES:
                image_file = request.FILES['picture']
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(filename)
                note.picture = uploaded_file_url[6:]
            note.save()

            group_id = request.POST.get('groups')
            if group_id:
                groups = MyGroup.objects.get(pk=group_id)
                note.groups.add(groups)

            return redirect('notes_list')  # Redirect to notes list page after saving
    else:
        form = NoteForm()
    return render(request, 'authentication/create_notes.html', {'form': form})



@login_required
def notes(request):
    notes = Note.objects.filter(owner = request.user.id)
    form = NoteForm()
    return render(request, 'authentication/notes.html', {'notes': notes, 'form': form})

def notes_list(request):
    categories = Category.objects.all()
    notes = Note.objects.filter(owner=request.user.pk)
    selected_category = request.GET.get('category')
    if selected_category:
        notes = notes.filter(category__id=selected_category)
    context = {'notes': notes, 'categories': categories, 'selected_category': selected_category}
    return render(request, 'authentication/notes_list.html', context)



@login_required
def update_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            if not note.category:  # jeśli kategoria nie została wybrana w formularzu
                note.category = note.category  # użyj domyślnej kategorii notatki
        note.save()
        return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    context = {'form': form, 'note': note}
    return render(request, 'authentication/update_note.html', context)



@login_required
def delete_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'authentication/delete_note.html', {'note': note})



