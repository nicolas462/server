from . import Database


def getClassSessionByNrcAndDay(nrc, day: int):
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT ID_CLASS_SESSION, END_TIME FROM CLASS_SESSION WHERE CLASS_NRC = '{nrc}' AND `DAY` = {day}")
  res = mycursor.fetchone()
  mycursor.close()
  #Database.mydb.close()
  return res

def getClassNameByNrc(nrc) -> str:
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT `NAME` FROM CLASS WHERE NRC = '{nrc}'")
  res = mycursor.fetchone()[0]
  mycursor.close()
  #Database.mydb.close()
  return res


