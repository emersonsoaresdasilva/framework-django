from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from webdev.tarefas.forms import TarefaNovaForm, TarefaForm
from webdev.tarefas.models import Tarefa

def home(request):
    if request.method == 'POST': # Caso os dados do formulário serem válidos.
        form = TarefaNovaForm(request.POST)
        if form.is_valid(): # São válidos?
            form.save() # Salva no banco de dados.
            return HttpResponseRedirect(reverse('tarefas:home')) # Redireciona para home de tarefas.
        else: # Não são válidos?
            tarefas_pendentes = Tarefa.objects.filter(feita=False).all()
            tarefas_feitas = Tarefa.objects.filter(feita=True).all()
            return render(
                request, 'tarefas/home.html',
                {
                    'form': form,
                    'tarefas_pendentes': tarefas_pendentes,
                    'tarefas_feitas': tarefas_feitas
                },
                status=400)
    tarefas_pendentes = Tarefa.objects.filter(feita=False).all()
    tarefas_feitas = Tarefa.objects.filter(feita=True).all()
    return render(
        request, 'tarefas/home.html',
        {
            'tarefas_pendentes': tarefas_pendentes,
            'tarefas_feitas': tarefas_feitas,
        })

def detalhe(request, tarefa_id):
    if request.method == 'POST':
        tarefa = Tarefa.objects.get(id=tarefa_id)
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('tarefas:home'))

def apagar(request, tarefa_id):
    if request.method == 'POST':
        Tarefa.objects.filter(id=tarefa_id).delete()
    return HttpResponseRedirect(reverse('tarefas:home'))