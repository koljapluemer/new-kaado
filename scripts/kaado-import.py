import os
from supabase import create_client, Client
from main.models import *
import datetime
from tqdm import tqdm

def import_cards():
    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('cards').select("*").execute()

    count_of_new_cards = 0 
    count_of_updated_cards = 0
    for row in tqdm(response.data):
        # check if card with same old_id already exists
        if Card.objects.filter(old_id=row['id']).exists():
            card = Card.objects.get(old_id=row['id'])
            count_of_updated_cards += 1
        else:
            card = Card()
            count_of_new_cards += 1
        # convert created at from '2023-02-07 19:28:26.10849+00' to DateTimeField
        created = row['created_at'].split('+')[0]
        card.created_at = created 
        card.front = row['front']
        card.back = row['back']
        type = row['type']
        if type == 'other' or type == 'standard' or type == '':
            type = 'misc'
        elif type == 'readingList':
            type = 'book'
        elif type == 'articleList':
            type = 'article'
        card.type = type
        card.is_active = True
        card.is_priority = row['priority']
        card.is_started = row['startedReading']
        card.ease = row['ease'] if row['ease'] else 1
        card.repetitions = row['repetition'] if row['repetition'] else 0
        card.occurrences = row['occurrences']
        card.interval = row['interval'] if row['interval'] else 1
        card.interval_unit = row['unit'][0] if row['unit'] else 'd'
        # convert from js timestamp in the style of "1695585013" to datetime
        card.due_at = datetime.datetime.fromtimestamp(float(row['nextShown'])/1000)

        card.old_id = row['id']
        old_user_id = row['user_id']
        card.old_user_id = old_user_id
        card.save()

        tag_from_collection = row['pack_id']
        if tag_from_collection:
            # get or create tag
            tag, created = Tag.objects.get_or_create(name=tag_from_collection, old_user_id=old_user_id)
            card.tags.add(tag)

def import_tags_from_collections():
    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('packs').select("*").execute()

    for row in tqdm(response.data):
        # find tag with id and rename with name from row, converted to format 'abc-123'
        if Tag.objects.filter(name=row['id']).exists():
            tag = Tag.objects.get(name=row['id'])
            tag.name = row['name'].replace(' ', '-').lower()
            tag.save()
            # if disabled, set all cards of this tag to is_active = False
            if row['isDisabled']:
                # filter cards where tag is in tags
                cards = Card.objects.filter(tags__in=[tag])
                for card in cards:
                    card.is_active = False
                    card.save()

def import_logs():

    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('scores').select("*").execute()

    for row in tqdm(response.data):
        log = Log()
        log.card = Card.objects.get(old_id=row['card_id']) if Card.objects.filter(old_id=row['card_id']).exists() else None
        log.created_at = row['created_at']
        log.score = row['value']
        log.type = row['type']
        log.old_id = row['id']
        # TODO: this should work i don't know why it wouldnt..
        log.input_type = row['input_type']
        log.skip_note = row['skip_note']
        log.card_front = row['card_front']
        log.old_user_id = row['user_id']
        log.save()

def import_connections():
    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('card_connections').select("*").execute()

    for row in tqdm(response.data):
        try:
            card_sender = Card.objects.get(old_id=row['card_sender'])
            card_receiver = Card.objects.get(old_id=row['card_receiver'])
            card_sender.connected_cards.add(card_receiver)
        except:
            print('some card does not exist')
def run():
    import_cards()
    import_tags_from_collections()
    import_logs()
    import_connections()