from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = "Envia lembrete para os membros do canal #quero-cafe desligarem a cafeteira."

    def handle(self, *args, **options):
        mensagem = "DESLIGAR A CAFETEIRA"

        #ENVIANDO MENSAGEM AO GRUPO DO SLACK
        url = 'https://hooks.slack.com/services/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'
        payload = {"channel": "#quero-cafe", "username": "Véi Do Café", "text": mensagem, "icon_emoji": ":coffee:"}
        response = requests.post(url, data=payload, headers={})