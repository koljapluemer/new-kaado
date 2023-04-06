import os
from supabase import create_client, Client
from main.models import *
import datetime


def run():

    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('cards').select("*").filter('user_id', 'eq', 'd421079d-8fb6-4c27-86c0-32210d81bb7d').execute()

    profile = Profile.objects.first()
    for row in response.data:
        card = Card()
        card.profile = profile
        # convert created at from '2023-02-07 19:28:26.10849+00' to DateTimeField
        created = row['created_at'].split('+')[0]
        card.created_at = created 
        card.front = row['front']
        card.back = row['back']
        card.type = row['type']
        card.is_active = True
        card.is_priority = row['priority']
        card.is_started = row['startedReading']
        card.ease = row['ease'] if row['ease'] else 1
        card.repetitions = row['repetition'] if row['repetition'] else 0
        card.occurrences = row['occurrences']
        card.interval = row['interval'] if row['interval'] else 1
        card.interval_unit = row['unit'][0] if row['unit'] else 'd'
        # convert from js  timestamp in the style of "1695585013" to datetime
        card.due_at = datetime.datetime.fromtimestamp(float(row['nextShown'])/1000)

        card.old_id = row['id']
        card.save()

        tag_from_collection = row['pack_id']
        if tag_from_collection:
            # get or create tag
            tag, created = Tag.objects.get_or_create(name=tag_from_collection, profile=profile)
            card.tags.add(tag)