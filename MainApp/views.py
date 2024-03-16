from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from django.http import HttpResponseNotFound
from MainApp.forms import SnippetForm


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            "pagename": "Добавление нового сниппета",
            "form": form,
        }
        return render(request, "pages/add_snippet.html", context)

    # Получаем данные из формы и на их основе создаем новый snippet в базе
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")
        return render(request, "add_snippet.html", {"form": form})


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


# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("snippets-list")
#         return render(request,'add_snippet.html', {'form': form})
