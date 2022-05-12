from . import Database

def getWhatsappNumberById(idStudent):
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT WHATSAPP_NUMBER FROM STUDENT WHERE ID_STUDENT={idStudent}")
  return f"57{mycursor.fetchone()[0]}"