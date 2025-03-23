from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def sum_reactions(posts):
    return sum(post.reactions.count() for post in posts)

@register.filter
def sum_comments(posts):
    return sum(post.comments.count() for post in posts)

@register.filter
def sum_votes(choices):
    return sum(choice.votes for choice in choices)

@register.filter
def filter_reactions(reactions, reaction_type):
    return reactions.filter(reaction_type=reaction_type)

@register.filter
def percentage(value, total):
    try:
        if total > 0:
            return round((value / total) * 100, 1)
        return 0
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def has_user_reacted(post, user):
    if not user.is_authenticated:
        return False
    return post.reactions.filter(user=user).exists()

@register.filter
def get_user_reaction_type(post, user):
    if not user.is_authenticated:
        return None
    reaction = post.reactions.filter(user=user).first()
    return reaction.reaction_type if reaction else None
