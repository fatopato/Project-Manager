from django import template
from core.views import is_analyst, is_developer, is_admin, is_project_manager

register = template.Library()


@register.filter(name='available_for_admin')
def available_for_admin(user):
    return is_admin(user)


@register.filter(name='available_for_project_manager')
def available_for_project_manager(user):
    return is_project_manager(user) or available_for_admin(user)


@register.filter(name='available_for_developer')
def available_for_developer(user):
    return available_for_project_manager(user) or is_developer(user)


@register.filter(name='available_for_analyst')
def available_for_analyst(user):
    return available_for_project_manager(user) or is_analyst(user)


@register.filter(name='available_for_member')
def available_for_member(user):
    return available_for_project_manager(user) or is_analyst(user) or is_developer(user)


