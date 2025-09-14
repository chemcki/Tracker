from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return dictionary[key] safely in templates."""
    return dictionary.get(key)