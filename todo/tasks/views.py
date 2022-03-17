from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import TaskForm

 
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = 'title'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list')

class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    #weryfikacja formularza 
    def form_valid(self, form):
        user = form.save() #tworzy obiekt w bazie wynikający z formularza
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # nie działa redirect_authenticated_user = True wiec nadpisuje
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super(RegisterPage, self).get(*args, **kwargs)   



# Create your views here.
class ListTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ('title',)
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'
    form = TaskForm
    
    success_url = reverse_lazy('list')

# zapisuje zadanie z ustawionym polem User - jako zalogowany użytkiwnik
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(ListTask, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(user=self.request.user) 
        return context
    
class UpdateTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = 'title','description','complete',
    context_object_name = 'item'
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Task.objects.get(id=self.kwargs['pk'])
        return context


def deleteTask(request, pk):
    
    item = Task.objects.get(id=pk)
    
    if request.method =='POST':
        item.delete()
        return redirect('/')
    
    context = {'item':item}    
    return render(request, 'tasks/delete.html',context)