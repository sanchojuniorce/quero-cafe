import re
from random import randint
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.core.management import call_command
from core.helpers.slack import Message

from django.contrib.auth.models import User
from coffee_rotation.models.Cycle import Cycle
from coffee_rotation.models.Turn import Turn


def list(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (reverse_lazy('admin:login'), request.path))

    cycle = Cycle.objects.last()

    if cycle is None:
        cycle = Cycle.objects.create(name='Ciclo 01')

    turns = Turn.objects.filter(cycle=cycle)

    calleds = turns.values_list('user', flat=True)

    not_calleds = User.objects.exclude(pk__in=calleds.filter(date_removed__isnull=True)).filter(is_active=True)

    return render(request, 'list.html', {
        'turns': turns,
        'not_calleds': not_calleds,
    })


def set_as_voluntary(request):

    try:
        user = request.user
        cycle = Cycle.objects.last()
        date_voluntary = datetime.now()

        Turn.objects.create(user=user, cycle=cycle, date_voluntary=date_voluntary)

        #ENVIANDO MENSAGEM AO GRUPO DO SLACK
        mensagem = "("+ user.first_name +" "+ user.last_name +") voluntariou-se para fazer o café."
        Message.send(text=mensagem)

        messages.success(request, 'Voluntariou-se com sucesso!')

    except ValueError as error:

        messages.error(request, error)

    return redirect(reverse_lazy('list'))


def remove_turn(request, id):

    try:
        if request.method != 'POST':
            raise ValueError('Requisição tem que ser POST')

        turn = Turn.objects.get(id=id)

        if turn.is_choosed() and request.user.id == turn.user_id:
            raise ValueError('Você não pode remover um turno no qual você foi escolhido')

        turn.date_removed = datetime.now()
        turn.justification = request.POST['justification']
        turn.removed_by_id = request.user.id

        turn.save()

        messages.success(request, 'Turno removido com sucesso!')

    except ValueError as error:

        messages.error(request, error)

    return redirect(reverse_lazy('list'))


def choose_randomly(request):

    try:
        call_command('choose_randomly')

        messages.success(request, 'Usuário escolhido com sucesso!')

    except ValueError as error:

        messages.error(request, error)

    return redirect(reverse_lazy('list'))