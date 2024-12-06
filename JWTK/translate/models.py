

# Create your models here.

"""
primary_key
default
blank
null

Charfield
Integerfield
FloatField
EmailField
Datefield
DateTimeField
EmailField
BooleanField


"""
from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Lesson {self.number}: {self.title}"

class Phrase(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='phrases')
    phrase = models.CharField(max_length=256, null= True)
    translation_fr = models.CharField(max_length=256, null= True)
    translation_en = models.CharField(max_length=256, default='default_value')
    translation_ru = models.CharField(max_length=256, null= True)
    phrase_number = models.IntegerField(null=True, blank=True, default=0, unique= False)
    # id = models.AutoField(primary_key=True)
    
    class Meta:
        unique_together = ('lesson', 'phrase_number')  # Unicité par leçon et numéro de phrase

    def __str__(self):
        return self.phrase

class Language(models.Model):
    language = models.CharField(max_length= 12)


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
        # Le modèle User est fourni par Django. 
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    phrases_worked_on = models.ManyToManyField(Phrase, blank=True)
        # Enregistre toutes les phrases travaillées par l'utilisateur dans cette leçon. 
    completed_phrases_count = models.PositiveIntegerField(default=0)
        # Compte le nombre de phrases étudiées dans cette leçon. 
        # Ce champ optimise les calculs pour éviter de compter chaque fois le nombre d'éléments dans phrases_worked_on.


    def update_progress(self, phrase):
        """Met à jour la progression de l'utilisateur pour une phrase spécifique."""
        if phrase not in self.phrases_worked_on.all():
            self.phrases_worked_on.add(phrase)
            self.completed_phrases_count += 1
            self.save()

    def __str__(self):
        return f"{self.user.username}'s progress in Lesson {self.lesson.number}"