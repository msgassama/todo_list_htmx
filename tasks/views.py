from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from .models import Collection, Task
from django.utils.html import escape
from django.utils.text import slugify
from django.urls import reverse

# Create your views here.

def index(request):
    context={}

    collection_slug = request.GET.get("collection")
    collection = Collection.get_default_collection()

    if not collection_slug:
        return redirect(f"{reverse('home')}?collection={collection.slug}")

    collection = get_object_or_404(Collection, slug=collection_slug)
    context['collections'] = Collection.objects.order_by("slug")
    context['collection'] = collection
    context["tasks"] = collection.task_set.order_by('description')
    
    return render(request, 'tasks/index.html', context=context)

def add_collection(request):
    collection_name = escape(request.POST.get("collection-name"))        
    collection, created = Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))
    if not created:
        return HttpResponse("La collection existe déjà", status=409)
    
    # return HttpResponse(f'<h2>{collection_name}</h2>')
    return render(request, 'tasks/collection.html', context={'collection':collection})

def add_task(request):
    
    collection =  Collection.objects.get(slug=request.POST.get('collection')) if request.POST.get("collection") != 'null' else Collection.get_default_collection()
    description=request.POST.get("task-description")
    task = Task.objects.create(description=description, collection=collection)


    # return HttpResponse(description)
    return render(request, 'tasks/task.html', context={'task':task})

def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()

    return HttpResponse("")


def delete_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    collection.delete()

    return redirect("home")


def get_tasks(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    tasks = collection.task_set.order_by("description")
    # return HttpResponse("<br>".join(task.description for task in tasks))
    return render(request, 'tasks/tasks.html', context={'tasks':tasks, "collection":collection})
