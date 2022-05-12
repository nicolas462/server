import requests
import json

__token__ = '8cwus248ah28kwuq'
__instance__ = ' https://api.chat-api.com/instance414467/'

def __getUrl__(request: str) -> str:
    return f'{__instance__}{request}?token={__token__}'

def sendMessage(phone: str, message: str) -> int:
    url = __getUrl__('sendMessage')
    #message dictionary structure
    messageDict = {
        "phone" : phone,
        "body" : message
    }
    r = requests.post(url, messageDict)
    statusResponseStr = json.loads(r.text)['sent']
    statusReponseInt = r.status_code
    
    if statusReponseInt != 200:
        return -1
    if not(statusResponseStr):
        return -1
    else:
        return 1

#return the last 100 messages in a dictionary format
def getMessagesByNumber(phone: str, time: int)-> dict:
    #last=true: last messages only
    #chatId=phone: only messages from number
    #min_time={time}: messages equals or greather than timeUnix given
    url = f'{__getUrl__("messages")}&last=true&chatId={phone}@c.us&min_time={time}'
    r = requests.get(url)
    return json.loads(r.text)['messages']