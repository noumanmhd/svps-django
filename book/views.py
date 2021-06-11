from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Slot


@login_required
def home(request):
    context = {}
    t = timezone.now()
    number = None
    context['name'] = request.user.get_full_name().title()
    slot = Slot.objects.filter(user=request.user, time__gt=t).first()
    if slot:
        t = slot.time
        number = slot.number
    timer = t.strftime("%B %d, %Y %T")
    context['timer'] = timer
    context['number'] = number

    return render(request, template_name='book/home.html', context=context)


@login_required
def profile(request):
    context = {}
    t = timezone.now()
    number = None
    context['name'] = request.user.get_full_name().title()
    slot = Slot.objects.filter(user=request.user, time__gt=t).first()
    if slot:
        t = slot.time
        number = slot.number
    timer = t.strftime("%B %d, %Y %T")
    context['timer'] = timer
    context['number'] = number
    context['sub_status'] = request.user.profile.subscription > timezone.now()
    return render(request, template_name='book/profile.html', context=context)


def fresh_login(request):
    messages.success(
        request, f'Welcome! {request.user.get_full_name().title()}')
    return redirect('home')


@login_required
def reserve(request, pk):
    check_1 = Slot.objects.filter(
        user__pk=request.user.pk, time__gt=timezone.now())
    check_2 = Slot.objects.filter(user__pk=request.user.pk, status=True)
    if check_1.count() == 0 and check_2.count() == 0:
        slot = Slot.objects.get(pk=pk)
        if slot.time < timezone.now() and not slot.status:
            slot.user = request.user
            slot.time = timezone.now() + timedelta(minutes=30)
            slot.save()
            messages.success(
                request, f"Slot [{slot.number}] is reserved for 30min!")
            return redirect('home')
        else:
            messages.error(
                request, f"Slot [{slot.number}] is already reserved!")
    else:
        if check_1.count() > 0:
            check = check_1.first()
        else:
            check = check_2.first()

        messages.error(
            request, f"You already have a reservation [{check.number}]!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SlotsListView(LoginRequiredMixin, ListView):
    model = Slot
    template_name = 'book/slots.html'

    def get_queryset(self):
        queryset = Slot.objects.none()
        check_1 = Slot.objects.filter(
            user__pk=self.request.user.pk, time__gt=timezone.now())
        check_2 = Slot.objects.filter(
            user__pk=self.request.user.pk, status=True)
        if check_1.count() == 0 and check_2.count() == 0:
            queryset = Slot.objects.filter(
                time__lt=timezone.now(), status=False)
        return queryset
