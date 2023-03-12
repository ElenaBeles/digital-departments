from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required

from web.forms import RegistrationForm, AuthForm, ArticleForm, TagForm
from web.models import Article, Tag

User = get_user_model()


def main_view(request):
    overall_stat = Article.objects.aggregate(
        count=Count("id"),
    )
    user_stat = Article.objects.all().filter(user=request.user)

    print(overall_stat)
    print(user_stat)

    return render(request, "web/main.html", {
        "overall_stat": overall_stat,
        "user_stat": user_stat,
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def article_edit_view(request, id=None):
    article = get_object_or_404(Article, user=request.user, id=id) if id is not None else None
    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES, instance=article, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/article_form.html", {"form": form})


@login_required
def article_delete_view(request, id):
    article = get_object_or_404(Article, user=request.user, id=id)
    article.delete()
    return redirect('main')


@login_required
def tags_view(request):
    tags = Tag.objects.all()
    form = TagForm()

    if request.method == 'POST':
        form = TagForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            redirect('tags')

    return render(request, "web/tags.html", {
        'tags': tags,
        'form': form
    })


@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(Tag, user=request.user, id=id)
    tag.delete()
    return redirect('tags')


@login_required
def analytics_view(request):
    overall_stat = Article.objects.aggregate(
        count=Count("id")
    )

    # days_stat = (
    #     TimeSlot.objects.exclude(end_date__isnull=True)
    #     .annotate(date=TruncDate("start_date"))
    #     .values("date")
    #     .annotate(
    #         count=Count("id"),
    #         realtime_count=Count("id", filter=Q(is_realtime=True)),
    #         spent_time=Sum(F("end_date") - F("start_date"))
    #     )
    #     .order_by('-date')
    # )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
    })
