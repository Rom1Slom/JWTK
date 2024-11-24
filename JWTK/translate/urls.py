from django.urls import path
from . import views

app_name = "translate"
# on nomme ici l'application, ça va permmettre d'isoler les app une à une

urlpatterns =[

    path('', views.index, name='index'), # traduire/
    path('accueil/', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('<int:phrase_lesson_id>/', views.show, name = "show"), # traduire/<id>
    path('traduction/<int:phrase_id>/', views.get_traduction, name='get_traduction'),
    path('traduction/', views.phrase_a_traduire, name='phrase_a_traduire'),  # Pour afficher la page HTML avec le bouton
    path('ajax/', views.my_view, name='my_view'),
    # path('lesson/<int:lesson_id>/', views.translate_lesson, name='translate_lesson'),
    path('signup/', views.signup, name='signup')

]
