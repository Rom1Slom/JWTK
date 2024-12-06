from .models import Lesson

def lesson_table_context(request):
    lessons = Lesson.objects.all().order_by('number')
    total_lessons = lessons.count()

    # Diviser les leçons en lignes (6 colonnes par défaut)
    columns = 6
    rows = [lessons[i:i + columns] for i in range(0, total_lessons, columns)]

    return {
        'rows': rows,  # Tableau des leçons
    }