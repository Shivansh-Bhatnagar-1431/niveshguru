from django.shortcuts import render

# Create your views here.
# tradeblog/views.py
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import TradePost
from .forms import TradePostForm
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = TradePost
    template_name = 'post_list.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = TradePost
    form_class = TradePostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = TradePost
    success_url = reverse_lazy('post_list')
    template_name = 'post_confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)