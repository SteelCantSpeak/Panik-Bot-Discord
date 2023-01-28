import mysql.connector

from lib import gSheetReference as sheet

def connect():
  try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="users"
  )
  except:
  #in case no db
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
  )
  return mydb
def createNew():
  mycursor.execute("CREATE DATABASE users")
  mycursor.execute("CREATE TABLE sheets (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), link VARCHAR(255))")

#USE COMMANDS
def importSheet(message):
  author = message.author.id
  link = message.content.split()

  #Check for existing record
  sql = "SELECT * FROM sheets WHERE link ='%s' AND name = %s;" % (link[1], author,)

  mycursor.execute(sql)

  resultCount = mycursor.fetchall() #number of Results
  if len(resultCount) >= 1:
    return ("Oops", "Your Sheet appears to already exist, please use `$char` to use that sheet", "$help")

#Insert (Author Name, Sheet Link,)
  sql = "INSERT INTO sheets (name, link) VALUES (%s, %s)"
  val = (author, link[1], )
  mycursor.execute(sql, val)

  mydb.commit() #Pressing Play on SQL Command

  print(mycursor.rowcount, "record inserted.")
  return getCharacter(link[1])

def listSheets(message):
  author = message.author.id #person checked
    #Check for existing record
  resultCount = characterlist(author) #ID, Author, Sheet ID, name

  list = ""
  array = 0
  if len(resultCount) > 0: #If there is a List of Characters
    for x in resultCount:
      row = sheet.getCharacterArray(sheet.getSheetLink(x[0]))
      list += "["+ str(array+1)+"] "+ sheet.getCharacterName(row) +"\n " #array number
      array +=1
  else:
    list += "You currently have no Characters. Attach one now using `$import [url]` now!"

  return ["Your Character List:", str(list),"$list • $char # to select a character"]

def setCurrent(message): #Set or create the ActiveCharacter for a User
  author = message.author.id
  content = message.content.split()

  charList = characterlist(author) 

  if len(content) > 1 and int(content[1]) < (len(charList)+1): #If there is listed Number and it's less than the number of sheets linked
    result = getActiveCharacter(author) #Check to see if there is currently an Active Character

    index = int(content[1])-1 #if asking for the first, it'll look for array pos 0
    activeChar = sheet.getSheetLink(charList[index][0]) #get the called for Character

    if len(result) > 0: #If there is a listed sheet, change, else add a new row
      sql = "UPDATE users SET sheetID= \"%s\" WHERE userID = %s;" % (activeChar, author,)
      mycursor.execute(sql)
      result = getActiveCharacter(author) 
    else:
      sql = "INSERT INTO users VALUES (%s, %s)"
      val = (author, activeChar,)
      mycursor.execute(sql, val)

      mydb.commit() #Pressing Play on SQL Command
  return getCharacter(getActiveCharacter(author)[1])

def rollSheet(message): #Roll the Dice for the Active Character
  author = message.author.id
  x = message.content.split() #the skill

  sheetID = getActiveCharacter(author)[1]
  charArray = sheet.getCharacterArray(sheetID)

  return sheet.rollFromSheet(charArray, x[1])
  #Get the Current Sheet



#SUB FUNCTIONS

def characterlist(author): #Get List of Characters attached to the User
  sql = "SELECT link FROM sheets WHERE name ='%s';" % (author,)
  mycursor.execute(sql)

  charList = mycursor.fetchall()
  return (charList)

def getActiveCharacter(author): #Get the current ActiveCharacter for that User
  sql = "SELECT * FROM users WHERE userID = %s;" % (author,)
  mycursor.execute(sql)
  return mycursor.fetchone() #should only be one for the user

def getCharacter(link):
  x = sheet.getCharacterArray(link)
  return sheet.getCharacterBio(x)

mydb = connect()
mycursor = mydb.cursor()