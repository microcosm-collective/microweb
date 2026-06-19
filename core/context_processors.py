def site_context(request):
    """
    Provide default template values used by shared layouts.

    Individual views can still override these in their render context.
    """

    return {
        'event_dates': None,
        'is_expired': False,
        'pagination': None,
        'rsvp_num_invited': 0,
        'site_section': 'microcosm',
        'skipparents': False,
        'skipself': False,
        'showForum': False,
        'unread': False,
        'user': None,
    }
