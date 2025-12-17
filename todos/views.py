from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Todo
import json


def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'index.html', context)


def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        
        if title:
            todo = Todo.objects.create(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date if due_date else None
            )
            return redirect('index')
    
    return render(request, 'add_todo.html')


def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.priority = request.POST.get('priority', 'medium')
        todo.due_date = request.POST.get('due_date') or None
        todo.save()
        return redirect('index')
    
    context = {
        'todo': todo,
    }
    return render(request, 'edit_todo.html', context)


def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        return redirect('index')
    
    context = {
        'todo': todo,
    }
    return render(request, 'delete_confirm.html', context)


@require_http_methods(["POST"])
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'completed': todo.completed})
    
    return redirect('index')


def search_todos(request):
    query = request.GET.get('q', '')
    if query:
        todos = Todo.objects.filter(
            title__icontains=query
        ) | Todo.objects.filter(
            description__icontains=query
        )
    else:
        todos = Todo.objects.all()
    
    context = {
        'todos': todos,
        'query': query,
    }
    return render(request, 'search_results.html', context)
