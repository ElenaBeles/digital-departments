from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Min, Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from web.forms import RegistrationForm, AuthForm

User = get_user_model()


def main_view(request):
    # timeslots = TimeSlot.objects.filter(user=request.user).order_by('-start_date')
    # current_timeslot = timeslots.filter(end_date__isnull=True).first()
    #
    # filter_form = TimeSlotFilterForm(request.GET)
    # filter_form.is_valid()
    # timeslots = filter_timeslots(timeslots, filter_form.cleaned_data)
    #
    # total_count = timeslots.count()
    # timeslots = (
    #     timeslots
    #     .prefetch_related("tags")
    #     .select_related("user")
    #     .annotate(tags_count=Count("tags"))
    #     .annotate_spent_time()
    # )
    # page_number = request.GET.get("page", 1)
    #
    # paginator = Paginator(timeslots, per_page=100)
    #
    # if request.GET.get("export") == 'csv':
    #     response = HttpResponse(
    #         content_type='text/csv',
    #         headers={"Content-Disposition": "attachment; filename=timeslots.csv"}
    #     )
    #     return export_timeslots_csv(timeslots, response)

    # return render(request, "web/main.html", {
    #     "current_timeslot": current_timeslot,
    #     'timeslots': paginator.get_page(page_number),
    #     "form": TimeSlotForm(),
    #     "filter_form": filter_form,
    #     'total_count': total_count
    # })

    return render(request, "web/main.html")


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
