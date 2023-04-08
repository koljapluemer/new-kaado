from main.models import *

def run():
    set_of_types = set()

    for card in Card.objects.all():
        # if type is 'other', 'standard' or '', rename it to misc
        # if type is 'readingList', rename it to book
        # if type is 'articleList', rename it to article
        if card.type == 'other' or card.type == 'standard' or card.type == '':
            card.type = 'misc'
            card.save()
        elif card.type == 'readingList':
            card.type = 'book'
            card.save()
        elif card.type == 'articleList':
            card.type = 'article'
            card.save()

        set_of_types.add(card.type)

    print(set_of_types)