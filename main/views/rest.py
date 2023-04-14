from rest_framework import generics
from ..models import *
from ..serializers import *
import random
from rest_framework.response import Response
from rest_framework import status

class APICardList(generics.ListCreateAPIView):
    # TODO: limit more elegantly
    queryset = Card.objects.all()[:100]
    serializer_class = CardSerializer

class APICardRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class APICardRandom(generics.ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        random_type = random.choice(
            ['productivity', 'misc', 'book', 'article', 'learn'])
        if random_type == 'productivity':
            # get a card thats either 'todo', 'habit', or 'check'
            card = Card.objects.filter(user_id=user_id, type__in=['todo', 'habit', 'check'], is_active=True, due_at__lte=timezone.now()
                                        ).order_by('?').first()
        elif random_type == 'book':
            number_of_started_books = Card.objects.filter(user_id=user_id, type='book', is_active=True, is_started=True
                                                        ).count()
            if number_of_started_books < 5:
                card = Card.objects.filter(user_id=user_id, type='book', is_active=True, is_started=False
                                            ).order_by('?').first()
                card.is_started = True
                card.save()
            else:
                card = Card.objects.filter(user_id=user_id, type='book', is_active=True, is_started=True, due_at__lte=timezone.now()
                                            ).order_by('?').first()
        else:
            card = Card.objects.filter(user_id=user_id, type=random_type, is_active=True, due_at__lte=timezone.now()
                                        ).order_by('?').first()

        if card is None:
            # try to get any card
            card = Card.objects.filter(user_id=user_id, is_active=True, due_at__lte=timezone.now()
                                        ).order_by('?').first()
            
        return [card]
    
    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(id=self.kwargs['user_id'])
            return super().get(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)