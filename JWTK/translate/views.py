from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader 
from .models import Phrase, Lesson, UserProgress
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
import random


# Create your views here.

def index(request):

    context = {"phrases": Phrase.objects.all()}
    return render(request, "translate/accueil.html", context)


def show(request, phrase_lesson_id):
    context = {"phrase": get_object_or_404(Phrase, phrase_lesson = phrase_lesson_id)}
    return render(request, "translate/show.html", context)


def phrase_a_traduire(request):
    phrases = Phrase.objects.all().order_by('phrase_number')  # Récupérer toutes les phrases triées par leur numéro
    if not phrases:
        raise Http404('No phrase available')
    
    # Récupérer le numéro de la phrase actuelle
    current_phrase_number = request.GET.get('current_phrase_number')
    if current_phrase_number is not None and current_phrase_number.isdigit():
        current_phrase_number = int(current_phrase_number)
        try:
            current_phrase = phrases.get(phrase_number=current_phrase_number)
        except Phrase.DoesNotExist:
            current_phrase = None
    else:
        current_phrase = None
        current_phrase_number = 0

    # Récupérer la phrase précédente ou suivante en fonction de la requête
    if request.GET.get('previous'):  # Si l'on veut la phrase précédente
        previous_phrase = phrases.filter(phrase_number__lt=current_phrase_number).order_by('-phrase_number').first()
        if previous_phrase:
            current_phrase = previous_phrase
            current_phrase_number = current_phrase.phrase_number
    else:  # Sinon on prend la phrase suivante
        next_phrase = phrases.filter(phrase_number__gt=current_phrase_number).order_by('phrase_number').first()
        if next_phrase:
            current_phrase = next_phrase
            current_phrase_number = next_phrase.phrase_number

    if not current_phrase:  # Si aucune phrase n'a été trouvée, on prend la première phrase
        current_phrase = phrases.first()
        current_phrase_number = current_phrase.phrase_number

    context = {  # Définir le contexte avant de l'utiliser
        'phrase': current_phrase,
        'current_phrase_number': current_phrase_number,
    }

    # Si la requête est une requête AJAX, on renvoie les données en HTML partiel
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'translate/accueil.html', context)
    
    # Sinon, on renvoie le template complet
    return render(request, 'translate/traduction.html', context)



def get_traduction(request, phrase_id):
    try:
        phrase = Phrase.objects.get(id=phrase_id)
        return JsonResponse({
            'phrase' : phrase.phrase,
            'traduction': phrase.translation_fr})
    except Phrase.DoesNotExist:
        raise Http404("Phrase not found")



def my_view(request):
    data = {
        "message" : "Her gün çalisiyorum"
    }
    return JsonResponse(data)


def accueil(request):
    # Créer une liste de nombres de 1 à 60
    cases = list(range(1, 61))
    # Découper la liste en sous-listes de 6 éléments pour former les lignes
    lignes = [cases[i:i + 6] for i in range(0, len(cases), 6)]
    # return render(request, 'translate/index.html', {'lignes': lignes})

    # Récupérer toutes les leçons et leur progression pour l'utilisateur
    lessons = Lesson.objects.all().order_by('number')
    progress_data = []
       
    # Split `progress_data` into chunks of 6
    def batch(iterable, batch_size):
        for i in range(0, len(iterable), batch_size):
            yield iterable[i:i + batch_size]

    batched_progress_data = list(batch(progress_data[:60], 6))

    for lesson in lessons:
        # Récupérer ou créer la progression de l'utilisateur pour chaque leçon
        user_progress, _ = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)

        # Compter les phrases dans chaque leçon et celles étudiées
        total_phrases = lesson.phrases.count()
        completed_phrases = user_progress.phrases_worked_on.count()
        progress_percentage = (completed_phrases / total_phrases * 100) if total_phrases > 0 else 0
        # Ajouter les données de progression
        progress_data.append({
            'lesson_number': lesson.number,
            'title': lesson.title,
            'progress_percentage': progress_percentage,
        })

    context = {"lessons": Lesson.objects.all(),
               'lignes': lignes, 
                'progress_data' : progress_data,
                 'batched_progress_data': batched_progress_data }

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

