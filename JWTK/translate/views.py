from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template import loader 
from .models import Phrase, Lesson, UserProgress
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from django.db.models import Count
import random
import logging
import pandas as pd


logger = logging.getLogger(__name__)
# Rechercher les doublons
duplicates = Phrase.objects.values('lesson', 'phrase_number').annotate(count=Count('id')).filter(count__gt=1)

for dup in duplicates:
    print(dup)

# Create your views here.

def index(request):
    context = {"phrases": Phrase.objects.all()}
    return render(request, "translate/accueil.html", context)


def show(request, phrase_lesson_id):
    context = {"phrase": get_object_or_404(Phrase, phrase_lesson = phrase_lesson_id)}
    return render(request, "translate/show.html", context)


def phrase_navigation(request, lesson_id, current_id):
    # Récupérer la leçon correspondante
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Récupérer toutes les phrases associées à cette leçon, triées par numéro
    lesson_phrases = current_lesson.phrases.order_by('phrase_number')
    total_phrases = lesson_phrases.count()

    # Récupérer la phrase actuelle
    current_phrase = lesson_phrases.filter(phrase_number=current_id).first()
    if not current_phrase:
        return HttpResponseNotFound("phrase non trouvée dans cette leçon")
    
    # Détremnine the ID of the next and previous phrase in the current lesson
    next_phrase = lesson_phrases.filter(phrase_number__gt=current_id).first()
    previous_phrase = lesson_phrases.filter(phrase_number__lt=current_id).last()

    next_id = next_phrase.phrase_number if next_phrase else lesson_phrases.first().phrase_number
    previous_id = previous_phrase.phrase_number if previous_phrase else lesson_phrases.last().phrase_number
    
    show_translation = 'translation' in request.GET

    context = {
        'phrase': current_phrase,
        'show_translation': show_translation,
        'total_phrases': total_phrases,
        'lesson': current_lesson,
        'next_id':next_id,
        'previous_id':previous_id,
    }

    return render(request, "translate/phrase_navigation.html", context)

def mark_lesson_completed (request, lesson_id):
    if request.method == "POST":
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.is_completed = True
        lesson.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error":'Méthode non autorisée'})



def my_view(request):
    data = {
        "message" : "Her gün çalisiyorum"
    }
    return JsonResponse(data)


def accueil(request):
  
    lessons = Lesson.objects.all().order_by('number')
    total_lessons = lessons.count()
    # Générer les cases : diviser les leçons en lignes de 6 colonnes par exemple
    columns = 6
    rows = [lessons[i:i + columns] for i in range(0, total_lessons, columns)]
    context = {'lessons': lessons,
               'rows':rows,
               'show_sidebar': True}
    
    return render(request, "translate/index.html", context)

# def translate_lesson(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     first_phrase = lesson.phrases.order_by('phrase_number').first()
#     return render(request, 'translate/traduction.html', {'lesson': lesson, 'phrase': first_phrase})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Charger le profil de l'utilisateur
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/traduction')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = SignUpForm()
    return render(request, 'translate/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/accueil')  # Rediriger vers la page d'accueil
            else:
                form.add_error(None, 'Nom d\'utilisateur ou mot de passe incorrect')
    else:
        form = LoginForm()
    return render(request, 'translate/login.html', {'form': form})


def import_phrases(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']

        # Lecture du fichie excel
        df = pd.read_excel(file)

        for index, row in df.iterrows():

            Phrase.objects.create(
                phrase_number = row['phrase_number'],
                phrase=row['phrase'],
                translation_fr=row['translation_fr'],
                lesson_id = row['lesson_id']
            )
        return HttpResponse("Les phrases ont été importées avec succès.")

    return render(request, 'translate/import_phrases.html')

def import_lessons(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return render(request, 'translate/import_phrase.html', {'error': 'Aucun fichier sélectionné.'})

        try:
            df = pd.read_excel(file)

            # Vérifier les colonnes nécessaires
            if not {'number', 'title'}.issubset(df.columns):
                return render(request, 'translate/import_phrase.html', {'error': 'Le fichier doit contenir les colonnes "number" et "title".'})

            # Importer les leçons
            for _, row in df.iterrows():
                Lesson.objects.update_or_create(
                    number=row['number'],
                    defaults={'title': row['title']}
                )

            return render(request, 'translate/import_phrase.html', {'success': 'Importation des leçons réussie !'})

        except Exception as e:
            return render(request, 'translate/import_phrase.html', {'error': f'Erreur lors de l\'importation des leçons : {str(e)}'})

    return render(request, 'translate/import_phrase.html')
