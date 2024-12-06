from django.urls import path
from . import views

app_name = "translate"
# on nomme ici l'application, ça va permmettre d'isoler les app une à une

urlpatterns =[

    path('', views.index, name='index'), # traduire/
    path('accueil/', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('<int:phrase_lesson_id>/', views.show, name = "show"), # traduire/<id>
    # path('traduction/<int:phrase_id>/', views.get_traduction, name='get_traduction'),
    # path('traduction/', views.phrase_a_traduire, name='phrase_a_traduire'),  # Pour afficher la page HTML avec le bouton
    path('ajax/', views.my_view, name='my_view'),
    path('lesson/<int:lesson_id>/phrase/<int:current_id>/', views.phrase_navigation, name='phrase_navigation'),
    path('import/phrases/', views.import_phrases, name='import_phrases'),
    path('import/lessons/', views.import_lessons, name='import_lessons'),
    path('mark_lesson_completed/<int:lesson_id>/', views.mark_lesson_completed, name='mark_lesson_completed'),   # URL de base sans paramètre
    
    # path('phrases/<int:current_id>/', views.phrase_navigation, name='phrase_navigation_with_id'),  # URL avec ID
    # path('lesson/<int:lesson_id>/', views.translate_lesson, name='translate_lesson'),
    # path('signup/', views.signup, name='signup')

]
