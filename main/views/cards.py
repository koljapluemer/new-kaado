from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Card
from django.urls import reverse_lazy

class CardListView(ListView):
    model = Card
    template_name = 'cards/list.html'
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class CardCreateView(CreateView):
    model = Card
    fields = ['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit']
    template_name = 'cards/edit.html'
    success_url = reverse_lazy('card_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardUpdateView(UpdateView):
    model = Card
    fields = ['front', 'back', 'type', 'tags', 'is_active', 'is_priority', 'is_started',  'interval', 'interval_unit']
    template_name = 'cards/edit.html'
    success_url = reverse_lazy('card_list')

    def form_valid(self, form):
        form.instance = self.request.user
        return super().form_valid(form)

class CardDeleteView(DeleteView):
    model = Card
    success_url = reverse_lazy('queue')
    template_name = 'cards/confirm_delete.html'