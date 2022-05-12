from . import Database

def addPuntution(idHistoricClassSession, responses, idStudent):
  mycursor = Database.mydb.cursor()
  sql = """INSERT INTO `PUNTUATION`
            (`ID_HISTORIC_CLASS_SESSION`,
            `Q1_RESPONSE`,
            `Q2_REPONSE`,
            `Q3_REPONSE`,
            `ID_STUDENT`)
            VALUES (%s, %s, %s, %s, %s);"""
  val = (idHistoricClassSession, responses[0], responses[1], responses[2], idStudent)
  mycursor.execute(sql, val)
  Database.mydb.commit()
  mycursor.close()
  #Database.mydb.close()  