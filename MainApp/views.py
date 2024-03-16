from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from django.http import HttpResponseNotFound


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)


def add_snippet_page(request):
    context = {"pagename": "Добавление нового сниппета"}
    return render(request, "pages/add_snippet.html", context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        "pagename": "Просмотр сниппетов",
        "snippets": snippets,
    }
    return render(request, "pages/view_snippets.html", context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    context = {
        "pagename": "Просмотр сниппета",
        "snippet": snippet,
    }
    return render(request, "pages/snippet_detail.html", context)
