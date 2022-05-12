from . import Database

class HistoricClassSession:
  id = 0

  def __init__(self):
    self.id = self.findLastIdRegistred() + 1

  def addHistoricClassSession(self, idClassSession, date):
    mycursor = Database.mydb.cursor()
    sql = """INSERT INTO `HISTORIC_CLASS_SESSION`
              (`ID_HISTORIC_CLASS_SESSION`,
              `ID_CLASS_SESSION`,
              `DATE`)
              VALUES (%s, %s, %s);"""
    val = (self.id, idClassSession, date)
    mycursor.execute(sql, val)
    Database.mydb.commit()
    mycursor.close()
    #Database.mydb.close()

  def findLastIdRegistred(self) -> int:
    mycursor = Database.mydb.cursor()
    mycursor.execute(f"SELECT MAX(ID_HISTORIC_CLASS_SESSION) FROM HISTORIC_CLASS_SESSION")
    res = mycursor.fetchone()[0]
    mycursor.close()
    #Database.mydb.close()
    return res