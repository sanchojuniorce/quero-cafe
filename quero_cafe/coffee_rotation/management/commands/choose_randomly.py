from django.core.management.base import BaseCommand

import re
from random import randint
from datetime import datetime

from core.helpers.slack import Message

from django.contrib.auth.models import User
from coffee_rotation.models import Turn
from coffee_rotation.models import Cycle


class Command(BaseCommand):
    help = "Comando escolhe um dos usuários que ainda não fizeram café."

    def handle(self, *args, **options):

        #SCHEDULES HOURS
        now = datetime.now()

        #ACTUAL CYCLE
        cycle = Cycle.objects.last()

        #VERIFIY LAST TURN HOUR
        if 'verify_last_turn' in options:

            schedules = {
                'morning': {
                    'start': now.replace(hour=0, minute=0, second=0),
                    'end': now.replace(hour=7, minute=59, second=59),
                },
                'afternoon': {
                    'start': now.replace(hour=8, minute=1, second=0),
                    'end': now.replace(hour=12, minute=59, second=59)
                }
            }

            schedule = None

            if schedules['morning']['start'] < now < schedules['morning']['end']:
                schedule = 'morning'

            if schedules['afternoon']['start'] < now < schedules['afternoon']['end']:
                schedule = 'afternoon'

            if schedule is not None:
                last_turn = Turn.objects.filter(cycle=cycle, date_removed__isnull=True).last()

                if last_turn is not None:
                    if schedules[schedule]['start'] < last_turn.get_date() < schedules[schedule]['end']:
                        raise ValueError('Um usuário já foi escolhido')

        #SEARCHING USERS NOT CHOOSED BEFORE
        turns = Turn.objects.filter(cycle=cycle)
        calleds = turns.filter(date_removed__isnull=True).values_list('user', flat=True)
        not_calleds = User.objects.exclude(pk__in=calleds).filter(is_active=True)

        if not not_calleds.count():
            cycle = Cycle.objects.create(name=re.sub('\d(?!\d)', lambda x: str(int(x.group(0)) + 1), cycle.name))
            not_calleds = User.objects.all().filter(is_active=True)

        #CHOOSED RANDOMLY
        choosed = not_calleds[randint(0, not_calleds.count() - 1)]

        #CREATING TURN
        Turn.objects.create(user=choosed, cycle=cycle, date_choosed=datetime.now())

        #ENVIANDO MENSAGEM AO GRUPO DO SLACK
        mensagem = "("+ choosed.first_name +" "+ choosed.last_name +") foi o escolhido para fazer o café."
        Message.send(text=mensagem)