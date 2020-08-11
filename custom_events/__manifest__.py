{
    'name': 'Events Sync With Calendar',
    'version': '13.0.1.0',
    'category': 'Events',
    'author': 'PPTS [India] Pvt.Ltd.',
    'website': 'https://www.pptssolutions.com',
    'summary': 'Events Sync With Calendar',
    'description': """
    Events Sync With Calendar
    """,
    'depends': ['base', 'website', 'event', 'website_event_questions', 'calendar'],
    'data': [
        'views/event_event_views.xml',
        'views/calendar_event_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
