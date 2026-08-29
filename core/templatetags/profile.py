from django import template
register = template.Library()

@register.inclusion_tag('block_profile.html',takes_context=True)
def profile(context, profile, **kwargs):

    if hasattr(profile,'item'):
        context['profile'] = profile
    else:
        context['profile'] = {'item': profile, 'item_type': 'profile'}

    context['no_icon'] = bool(kwargs.get('no_icon', False))
    context['send_message'] = bool(kwargs.get('send_message', False))

    return context
