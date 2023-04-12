from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ..models import Tag
from django.urls import reverse_lazy

class TagListView(ListView):
    model = Tag
    template_name = 'tags/list.html'
    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

class TagCreateView(CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/edit.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/edit.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        form.instance = self.request.user
        return super().form_valid(form)
    
class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list')
    template_name = 'tags/confirm_delete.html'