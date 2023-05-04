
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from studnot.settings import MEDIA_ROOT
from .forms import NoteForm
from .models import Note, Category
from django.core.files.storage import FileSystemStorage




# Create your views here.
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


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        messages.success(request, "Twoje konto zostało poprawnie założone")
            
            
        return redirect('signin')
            
            
    else:
        form = NoteForm()
        data = {
            'username': '',
            'fname': '',
            'lname': '',
            'email': '',
            'pass1': '',
            'pass2': ''
        }
        return render(request, "authentication/signup.html", {'form': form, 'data': data})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Zalogowano poprawnie")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect('signin')
    
    return render(request, "authentication/signin.html")


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
            note.owner = request.user.username
            if 'picture' in request.FILES:
                image_file = request.FILES['picture']
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(filename)
                note.picture = uploaded_file_url[6:]
            note.save()
            return redirect('notes_list')  # Redirect to notes list page after saving
    else:
        form = NoteForm()
    return render(request, 'authentication/create_notes.html', {'form': form})



@login_required
def notes(request):
    notes = Note.objects.filter(owner = request.user.username)
    form = NoteForm()
    return render(request, 'authentication/notes.html', {'notes': notes, 'form': form})

def notes_list(request):
    notes = Note.objects.filter(owner=request.user)
    context = {'notes': notes}
    return render(request, 'authentication/notes_list.html', context)

def update_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            picture_action = request.POST.get('picture_action')  # pobranie wartości przycisku wyboru akcji
            if picture_action == 'delete' and note.picture:
                note.picture.delete()  # usunięcie pliku z dysku
                note.picture = None  # ustawienie wartości na None
            note = form.save(commit=True)
            if not note.category:  # jeśli kategoria nie została wybrana w formularzu
                note.category = note.category  # użyj domyślnej kategorii notatki
        note.save()
        return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    context = {'form': form, 'note': note}
    return render(request, 'authentication/update_note.html', context)




def delete_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')
    return render(request, 'authentication/delete_note.html', {'note': note})



