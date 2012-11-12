from bitdeli import Profiles, set_theme, Description, Title
from itertools import chain
from datetime import datetime

WINDOW = 48
text = {}

set_theme('playground')

def date(hour):
    return datetime.utcfromtimestamp(hour * 3600).strftime('%B %d, %Y')

def total_count(profiles):
    text['total'] = total = sum(1 for profile in profiles)
    yield {'type': 'text',
           'label': 'Total number of profiles',
           'size': (6, 3),
           'data': {'head': total}}

def new_profiles(profiles):
    def stats():
        for profile in profiles:
            events = profile['events'].itervalues()
            hours = [hour for hour, count in chain.from_iterable(events)]
            yield max(hours), min(hours)
    data = list(stats())
    text['newest'] = date(max(data)[0])
    text['oldest'] = date(min(first_event for last_event, first_event in data))
    limit = max(data)[0] - WINDOW
    text['num_new'] = num = sum(1 for last_event, first_event in data
                                if first_event > limit)
    text['since'] = tstamp = date(limit)
    yield {'type': 'text',
           'label': 'New profiles since %s' % tstamp,
           'size': (6, 3),
           'color': 2,
           'data': {'head': num}}

Profiles().map(total_count).show()
Profiles().map(new_profiles).show()

Title('{num_new:,} new user profiles added since {since}', text)

Description("""
The profile database contains {total:,} user profiles. The oldest stored event is from {oldest} and the newest from {newest}.
""", text)
