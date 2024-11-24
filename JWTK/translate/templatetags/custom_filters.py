from django import template

register = template.Library()

@register.filter
# def batch(iterable, size):
#     """Divise une liste en sous-listes de taille spécifiée."""
#     iterable = list(iterable)
#     return [iterable[i:i + size] for i in range(0, len(iterable), size)]
def color_from_progress(progress_percentage):
    """Calculates the HSL hue based on progress percentage."""
    # Convert percentage to a value from 0 to 120 for the hue
    hue = 120 * progress_percentage / 100
    return f"hsl({int(hue)}, 80%, 50%)"