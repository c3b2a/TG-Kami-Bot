from django import template

register = template.Library()

@register.simple_tag
def listToString(List):
	return ', '.join(List)
