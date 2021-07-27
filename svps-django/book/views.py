import json 
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
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
    slot_pk = 100
    context['name'] = request.user.get_full_name().title()
    slot = Slot.objects.filter(user=request.user, time__gt=t).first()
    if slot:
        t = slot.time
        number = slot.number
        slot_pk = slot.pk
    timer = t.strftime("%B %d, %Y %T")
    context['timer'] = timer
    context['number'] = number
    context['slot_pk'] = slot_pk

    return render(request, template_name='book/home.html', context=context)


@login_required
def profile(request):
    context = {}
    t = timezone.now()
    number = None
    slot_pk = 100
    context['name'] = request.user.get_full_name().title()
    slot = Slot.objects.filter(user=request.user, time__gt=t).first()
    if slot:
        t = slot.time
        number = slot.number
        slot_pk = slot.pk
    timer = t.strftime("%B %d, %Y %T")
    context['timer'] = timer
    context['number'] = number
    context['slot_pk'] = slot_pk
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


@login_required
def release(request, pk):
    check = Slot.objects.filter(
        user__pk=request.user.pk, time__gt=timezone.now())
    if check.count() >  0 :
        slot = Slot.objects.get(pk=pk)
        if slot.time > timezone.now() and not slot.status:
            slot.user = request.user
            slot.time = timezone.now()
            slot.save()
            messages.success(
                request, f"Slot [{slot.number}] is released!")
            return redirect('home')
        else:
            messages.error(
                request, f"Slot [{slot.number}] is already released!")
    else:
        messages.error(
            request, f"Unable to release!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_state(request):
    if request.META.get('REMOTE_ADDR') == '127.0.0.1':
        data = json.loads(request.body.decode('utf-8'))
        for k,v in data.items():
            slot = Slot.objects.filter(number=k).first()
            print(f"{k}: {v}")
            if slot:
                slot.status = v
                slot.save()
        return HttpResponse('',  status=200)
    return HttpResponse('',  status=201)

def check_plate(request):
    if request.META.get('REMOTE_ADDR') == '127.0.0.1':
        data = json.loads(request.body.decode('utf-8'))
        
        plates = Slot.objects.filter(
        user__profile__plate__icontains=data['plate'], time__gt=timezone.now())
        if plates.count() > 0:
            return HttpResponse('',  status=200)
    return HttpResponse('',  status=201)

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
