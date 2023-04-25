from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Card, Tag
from django.core import serializers
from django.urls import reverse_lazy
import json
import csv
from django.http import HttpResponse

class CardListView(ListView):
    model = Card
    template_name = 'cards/list.html'
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class CardCreateView(CreateView):
    model = Card
    fields = ['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit']
    template_name = 'cards/edit.html'
    success_message = "Card was created successfully"
    success_url = reverse_lazy('queue')

    # append all tags to the form 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # flatten queryset into a list of tag.name strings
        tags = Tag.objects.filter(user=self.request.user).values_list('name', flat=True)
        # serialize python list
        context['tags'] = json.dumps({'tags': list(tags)})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardUpdateView(UpdateView):
    model = Card
    fields = ['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit']
    template_name = 'cards/edit.html'
    success_message = "Card was edited successfully"
    success_url = reverse_lazy('queue')

    # append all tags to the form 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # flatten queryset into a list of tag.name strings
        tags = Tag.objects.filter(user=self.request.user).values_list('name', flat=True)
        # serialize python list
        context['tags'] = json.dumps({'tags': list(tags)})
        print('PASSING: ', self.object)
        context['state'] = serializers.serialize('json', [self.object])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class CardDeleteView(DeleteView):
    model = Card
    success_url = reverse_lazy('queue')
    template_name = 'cards/confirm_delete.html'

def export_cards_as_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cards.csv"'
    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    writer.writerow(['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit'])
    cards = Card.objects.filter(user=request.user)
    for card in cards:
        tags = ' '.join([tag.name for tag in card.tags.all()])
        writer.writerow([card.front, card.back, card.type, tags, card.is_active, card.is_priority, card.is_started, card.interval, card.interval_unit])
    return response
