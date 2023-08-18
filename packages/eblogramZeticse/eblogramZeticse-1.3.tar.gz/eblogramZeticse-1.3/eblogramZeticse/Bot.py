import requests
import json
общага = 'https://api.telegram.org/bot'

class Ты():
    def __init__(self, ктотывоин: str):
        self.рожденный = f'{общага}{ктотывоин}'
        self.спидознуть = self.рожденный + '/sendMessage?'
        self.порешать_базарик = self.рожденный + '/editMessageText?'
        self.ну_ты = self.рожденный + '/getMe'


    async def спиздануть(self, комната: int, словечко: str, в_ответ: int = None, 
        убрать_линк: bool = False, парсер: str = 'HTML', без_звука: bool = False):
        if без_звука is False:
            без_звука = '&disable_notification=0'
        else:
            без_звука = '&disable_notification=1'
        парсер = f'&parse_mode={парсер}'
        if убрать_линк is False:
            убрать_линк = '&disable_web_page_preview=0'
        else:
            убрать_линк = '&disable_web_page_preview=1'
        if в_ответ is None:
            ответ_от_дурова = requests.get(f'{self.спидознуть}chat_id={комната}&text={словечко}{убрать_линк}{парсер}')
        else:
            ответ_от_дурова = requests.get(f'{self.спидознуть}chat_id={комната}&text={словечко}&reply_to_message_id={в_ответ}{убрать_линк}{парсер}')

        норм_ответ = ответ_от_дурова.json()
        if норм_ответ['ok'] is False:
            raise Exception(норм_ответ['description'])
        return json.dumps(норм_ответ['result'], indent=4,  ensure_ascii=False)

    async def испр_базар(self, комната: int, базар_ид: int, новый_базар: str, парсер: str = 'HTML'):
        парсер = f'&parse_mode={парсер}'
        ответ_от_дурова = requests.get(f'{self.порешать_базарик}chat_id={комната}&message_id={базар_ид}&text={словечко}{парсер}')
        норм_ответ = ответ_от_дурова.json()
        if норм_ответ['ok'] is False:
            raise Exception(норм_ответ['description'])
        return json.dumps(норм_ответ['result'], indent=4,  ensure_ascii=False)

    async def кто_я(self):
        ответ_от_дурова = requests.get(self.ну_ты)
        норм_ответ = ответ_от_дурова.json()
        if норм_ответ['ok'] is False:
            raise Exception(норм_ответ['description'])
        return json.dumps(норм_ответ['result'], indent=4,  ensure_ascii=False)