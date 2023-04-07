import os
from supabase import create_client, Client
from main.models import *
import datetime

# Run cards first!

def run():

    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    response = supabase.table('packs').select("*").filter('user_id', 'eq', 'd421079d-8fb6-4c27-86c0-32210d81bb7d').execute()

    profile = Profile.objects.first()
    for row in response.data:
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
                    print(f"Disabled card {card.front[:30]}")
