from email import message
from urllib import response
from . import WhatsappApi
import time

class Poll:
    professor = ''
    matter = ''
    whatsappNumber = ''
    __wrongResponse__ = '❗Ooops! Recuerda responder del *1* al *10* sin decimales. Intentos restantes: '
    __notResponse__ = ("😓 No obtuvimos respuesta en esta ocasión. ¡No te preocupes! Será para la próxima."
            "\n🤓📘 Recuerda que con tu contestación estás contribuyendo a la *mejora de tu programa.*")
    __thanksMessage__ = '🤓📗✅ ¡Gracias por contribuir con tu respuestas para la mejora del programa! Mucha suerte en tu período académico.'

    def __init__(self, professor, matter, whatsappNumber):
        self.professor = professor
        self.matter = matter
        self.whatsappNumber = whatsappNumber

    def getLastMessage(self, lastMessageUnixTime: int, oldIdMessage: str) -> dict:
        counter = 0
        while counter < 30:
            time.sleep(1)
            messages = WhatsappApi.getMessagesByNumber(self.whatsappNumber, lastMessageUnixTime)
            #filter and take the time of the last message that has been sent to Whatsapp Server of the whatsapp number
            messagesReceived = list(filter(lambda x: x['fromMe'] in [False], messages))
            #filter by only text messages, not docs, images, audios, ...
            messagesReceived = list(filter(lambda x: x['type'] in ['chat'], messagesReceived))
            #if newLastMessage is not empty
            if bool(messagesReceived):
                if messagesReceived[-1]['id'] != oldIdMessage:
                    return messagesReceived[-1]
            counter = counter + 1
        return {}

    def getPollResponseInt(self, question: str) -> int:
        oldIdMessage = ''
        lastMessageUnixTime = time.time()
        time.sleep(3)
        WhatsappApi.sendMessage(self.whatsappNumber, question)
        for x in range (3):
            try:
                reponseMessage = self.getLastMessage(lastMessageUnixTime, oldIdMessage)
                #not new message
                if not bool(reponseMessage):
                    WhatsappApi.sendMessage(self.whatsappNumber, self.__notResponse__)
                    return -1
                elif reponseMessage['id'] != oldIdMessage:
                    if int(reponseMessage['body']) > 0 and int(reponseMessage['body']) < 11:
                        return int(reponseMessage['body'])
                    else:
                        if x < 2:
                            #lastMessageUnixTime = reponseMessage['time']
                            WhatsappApi.sendMessage(self.whatsappNumber, f'{self.__wrongResponse__}*{2-x}*')
                            oldIdMessage = reponseMessage['id']
                        else:
                            WhatsappApi.sendMessage(self.whatsappNumber, self.__notResponse__)
                            return -1
                        
            except ValueError:
                if x < 2:
                    #lastMessageUnixTime = reponseMessage['time']
                    WhatsappApi.sendMessage(self.whatsappNumber, f'{self.__wrongResponse__}*{2-x}*')
                    oldIdMessage = reponseMessage['id']
                else:
                    WhatsappApi.sendMessage(self.whatsappNumber, self.__notResponse__)
                    return -1
        return -1

    def getPollResponseStr(self, question: str) -> dict:
        oldIdMessage = ''
        lastMessageUnixTime = time.time()
        time.sleep(3)
        WhatsappApi.sendMessage(self.whatsappNumber, question)
        for x in range (3):
            reponseMessage = self.getLastMessage(lastMessageUnixTime + 1, oldIdMessage)
            if not bool(reponseMessage):
                WhatsappApi.sendMessage(self.whatsappNumber, self.__thanksMessage__)
                return {
                    'response': False,
                    'message': ''
                }
            else:
                WhatsappApi.sendMessage(self.whatsappNumber, self.__thanksMessage__)
                return {
                    'response': True,
                    'message': reponseMessage['body']
                }
        return -1

    def sendPoll(self):
        print("Sending poll to.........", self.whatsappNumber)
        questions = (
            {
            "id": 0,
            "question": f'🤓 ¿Del *1* al *10*, cuán satisfecho estás con la clase 📚 *{self.matter}* de hoy a cargo de 👩🧑 *{self.professor}*?',
            "response": -1
            },
            {
            "id": 1,
            "question": '🤔 Califica, del *1* al *10*, la utilidad de las temáticas vistas y/o los ejercicios realizados.',
            "response": -1
            },
            {
            "id": 2,
            "question": '🙌 ¡Genial! Déjanos saber tus comentarios adicionales 👇',
            "response": -1
            }
        )
        wellResponsed = True
        for x in range(2):
            responseValue = self.getPollResponseInt(questions[x]['question'])
            if responseValue == -1:
                wellResponsed = False
                return []
            else:
                questions[x]['response'] = responseValue
        if wellResponsed:
            strResponse = self.getPollResponseStr(questions[2]['question'])
            if strResponse['response'] == True:
                questions[2]['response'] = strResponse['message']
            else:
                questions[2]['response'] = ""

        return [questions[0]['response'], questions[1]['response'], questions[2]['response']]