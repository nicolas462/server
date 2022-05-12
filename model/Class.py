from . import Database


def getClassSessionByNrcAndDay(nrc, day: int):
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT ID_CLASS_SESSION, END_TIME FROM CLASS_SESSION WHERE CLASS_NRC = '{nrc}' AND `DAY` = {day}")
  return mycursor.fetchone()

def getClassNameByNrc(nrc) -> str:
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT `NAME` FROM CLASS WHERE NRC = '{nrc}'")
  return mycursor.fetchone()[0]


