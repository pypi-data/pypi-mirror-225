import requests

общага = 'https://api.telegram.org/bot'

class Ты():
    def __init__(self, ктотывоин: str):
        self.рожденный = f'{общага}{ктотывоин}'
        self.спидознуть = self.рожденный + '/sendMessage?'

    class CustomException(Exception):
        def __init__(self, description):
            self.description = description
            super().__init__(description)


    async def спиздануть(self, комната: int, словечко: str, в_ответ: int = None):
        if в_ответ is None:
            ответ_от_дурова = requests.get(f'{self.спидознуть}chat_id={комната}&text={словечко}')
        else:
            ответ_от_дурова = requests.get(f'{self.спидознуть}chat_id={комната}&text={словечко}&reply_to_message_id={в_ответ}')

        if ответ_от_дурова.status_code == 200:
            норм_ответ = ответ_от_дурова.json()
            if норм_ответ['ok'] is False:
                raise Exception(норм_ответ['description'])
            return норм_ответ['result']
        else:
            raise Exception(f'бля братан, хуета:{response.status_code}')
