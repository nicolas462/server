from model import Class, Professor, Student, Puntuation
from model.HistoricClassSession import HistoricClassSession
from model.Poll import Poll
import datetime, time
import pytz
from pytz import timezone
from datetime import datetime
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
tz = pytz.timezone('America/Bogota')

def getCurrentDate():
  return  datetime.now(tz)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/send-poll', methods=['POST'])
def get_poll_data():
    try:
        currentDate = getCurrentDate()
        content = request.json
        schedulePoll = content['schedule']
        class_nrc = content['nrc']
        attendance_list = content['attendance']
        #call class to know what class is (depends on day)
        idClassSession = Class.getClassSessionByNrcAndDay(class_nrc, int(currentDate.weekday()) + 1)
        endTimeClass = tz.localize(idClassSession[1])
        #wait until class finishes
        if endTimeClass.time() > currentDate.time() or not(schedulePoll):
            #create historic class session
            hCS = HistoricClassSession()
            hCS.addHistoricClassSession(idClassSession[0], (f"{currentDate.year}-{currentDate.day}-{currentDate.day}"))
            #get response
            professorName = Professor.findProfessorNameByNrc(class_nrc)
            matter = Class.getClassNameByNrc(class_nrc)
            threads = list()
            for idStudent in attendance_list.split(','):
                whatsappNumber = Student.getWhatsappNumberById(idStudent)
                poll = Poll(professorName, matter, whatsappNumber)
                #function to wait
                t = threading.Thread(target=asyncSendingPoll, args=(poll, hCS.id, idStudent, schedulePoll, endTimeClass, currentDate))
                threads.append(t)
                t.start()
            return 'Request processed successfully.', 201
    except Exception as e:
        return e, 402
    else:
        return 'The class session has already ended.', 401

def asyncSendingPoll(poll, historicClassSessionId, idStudent, schedulePoll, endTimeClass, currentDate):
    if schedulePoll:
        secondsLeft = endTimeClass - currentDate
        time.sleep(secondsLeft.seconds)
    responses = poll.sendPoll()
    #save responses with id_student and id_historic_class_session
    if responses:
        Puntuation.addPuntution(historicClassSessionId, responses, idStudent)

if __name__ == '__main__':
     app.run(debug=True)