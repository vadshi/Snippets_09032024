from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from django.http import Http404, HttpResponseNotFound
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        "pagename": "Мои сниппеты",
        "snippets": snippets,
        "count": snippets.count()
    }
    return render(request, "pages/view_snippets.html", context)


@login_required(login_url="home")
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
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
                messages.success(request, "New snippet has saved.")
            return redirect("snippets-list")
        return render(request, "pages/add_snippet.html", {"form": form})


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
        "pagename": "Просмотр сниппетов",
        "snippets": snippets,
        "type": "view",
        "count": snippets.count()
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
        "type": "view",
    }
    return render(request, "pages/snippet_detail.html", context)


@login_required
def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404

    # Variant 1
    # ==== Получение сниппета для редактирования с помощью SnippetForm ====
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request, "pages/add_snippet.html", {"form": form})
    # =====================================================================

    # Variant 2
    # Хотим получить страницу данных сниппета
    if request.method == "GET":
        context = {
            "pagename": "Просмотр сниппета",
            "snippet": snippet,
            "type": "edit",
        }
        return render(request, "pages/snippet_detail.html", context)

    # Хотим использовать данные из формы и сохранить изменения в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        if change_date := data_form.get("creation_date"):
            snippet.creation_date = change_date
        snippet.public = data_form.get("public", False)
        snippet.save()
        messages.success(request, "Snippet has changed.")
        return redirect("snippets-list")


@login_required
def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return redirect("snippets-list")


def create_user(request):
    context = {"pagename": "Регистрация пользователя"}
    # Пустая форма для заполнения данных
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request, "pages/registration.html", context)
    
    # Используем данные из формы
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context["form"] = form
        return render(request, "pages/registration.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'{username} logged in')
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["wrong username or password"],
            }
            return render(request, "pages/index.html", context)
    return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect("home")
