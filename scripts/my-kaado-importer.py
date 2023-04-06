from main.models import *
import csv
import datetime 

def run():
    profile = Profile.objects.first()

    with open('my_cards.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        #"enum","created_at","front","back","type","ease","interval","repetition","unit","user_id","nextShown","pack_id","id","occurrences","priority","startedReading"
        next(reader) 
        for row in reader:
            # if row has full data
                card = Card()
                card.profile = profile
                # convert created at from '2023-02-07 19:28:26.10849+00' to DateTimeField
                created = row[1].split('+')[0]
                card.created_at = created 
                card.front = row[2]
                card.back = row[3]
                card.type = row[4]
                card.is_active = True
                card.is_priority = row[14].lower() == 'true'
                card.is_started = row[15].lower() == 'true'
                # catch 'null' values
                card.ease = row[5] if row[5] != 'null' else 1
                card.repetitions = row[7] if row[7] != 'null' else 0
                card.occurrences = row[13]
                card.interval = row[6] if row[6] != 'null' else 1
                card.interval_unit = row[8][0]
                # convert from js  timestamp in the style of "1695585013" to datetime
                card.due_at = datetime.datetime.fromtimestamp(float(row[10])/1000)
                card.save()

                tag_from_collection = row[11]
                if tag_from_collection:
                    # get or create tag
                    tag, created = Tag.objects.get_or_create(name=tag_from_collection, profile=profile)
                    card.tags.add(tag)