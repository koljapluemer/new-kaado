import os
from supabase import create_client, Client
from main.models import *
import datetime


def run():

    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('scores').select("*").filter('user_id', 'eq', 'd421079d-8fb6-4c27-86c0-32210d81bb7d').execute()

    profile = Profile.objects.first()
    for row in response.data:
        log = Log()
        log.profile = profile
        log.card = Card.objects.get(old_id=row['card_id']) if Card.objects.filter(old_id=row['card_id']).exists() else None
        log.created_at = row['created_at']
        log.score = row['value']
        log.type = row['type']
        log.old_id = row['id']
        # TODO: this should work i don't know why it wouldnt..
        log.input_type = row['input_type']
        log.skip_note = row['skip_note']
        log.card_front = row['card_front']
        log.save()