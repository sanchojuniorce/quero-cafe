import requests
import subprocess

class Message:

    def send(text, username="CAFEITICEIRA", emoji=":coffee:", channel="#quero-cafe"):

        # proxies = {
        #     'http': 'http://proxy.defensoria.ce.def.br:3128/',
        #     'https': 'http://proxy.defensoria.ce.def.br:3128/',
        # }
        #
        # url = 'https://hooks.slack.com/services/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'
        # payload = { "channel": channel, "username": username, "text": text, "icon_emoji": emoji }
        #
        # response = requests.get(url, data=payload, proxies=proxies, headers={})
        #
        # return response

        CMD = 'curl -X POST --data-urlencode \'payload={"channel": "'+ channel +'", "username": "'+ username +'", "text": "'+ text +'", "icon_emoji": "'+ emoji +'"}\' https://hooks.slack.com/services/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 --proxy http://proxy.defensoria.ce.def.br:3128/'
        subprocess.call(CMD, shell=True)

        return