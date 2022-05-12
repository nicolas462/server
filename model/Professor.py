from . import Database

def findProfessorNameByNrc(nrc) -> str:
  mycursor = Database.mydb.cursor()
  mycursor.execute(f"SELECT CONCAT(`NAME`, CONCAT(' ',SURNAME)) FROM PROFESSOR WHERE ID_PROFESSOR=(SELECT ID_PROFESSOR FROM PROFESSOR_CLASS WHERE NRC={nrc})")
  res = mycursor.fetchone()[0]
  mycursor.close()
  #Database.mydb.close()  
  return res