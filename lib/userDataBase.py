import mysql.connector

from lib import gSheetReference as sheet

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
  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE users")
  mycursor.execute("CREATE TABLE sheets (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), link VARCHAR(255))")

mycursor = mydb.cursor()

def importSheet(message):
  author = message.author.id
  link = message.content.split()
  print(link[1])

  #Check for existing record
  sql = "SELECT * FROM sheets WHERE link ='%s' AND name = %s;" % (link[1], author,)

  mycursor.execute(sql)

  resultCount = mycursor.fetchall() #number of Results
  if len(resultCount) >= 1:
    return ("Oops", "Your Sheet appears to already exist, please use `$use [Name]` to use that sheet", "$help")

#Insert (Author Name, Sheet Link,)
  sql = "INSERT INTO sheets (name, link, charName) VALUES (%s, %s, %s)"
  charName = sheet.searchSheet("Name", link[1])
  val = (author, link[1], charName[0][0], )
  mycursor.execute(sql, val)

  mydb.commit() #Pressing Play on SQL Command

  print(mycursor.rowcount, "record inserted.")
  setCurrent(author, link[1])
  return getCharacter()


def listSheets(message):
  author = message.author.id #person checked
    #Check for existing record
  sql = "SELECT * FROM sheets WHERE name ='%s';" % (author,)

  mycursor.execute(sql)

  resultCount = mycursor.fetchall() #number of Results

  list = ""
  if len(resultCount) > 0:
    for x in resultCount:
      row = sheet.searchSheet("Name", x[2])
      list += str(row[0][0]) +", " #array number
  else:
    list += "You currently have no Characters. Attach one now using `$import [url]` now!"

  return ["Your Character List:", str(list),"$list"]

def getCurrent(message):
  author = message.author.id
  content = message.content.split()

  if len(content) >1:
    #Has Listed Character
    
    sql = "SELECT * FROM sheets WHERE charName ='%s' AND name = %s;" % (content[1], author,) #Gets the Active result

    mycursor.execute(sql)

    result = mycursor.fetchall()
    print(result)
    setCurrent(author, result[0])


def setCurrent(author, link =""):
  sql = "SELECT * FROM users WHERE userID = %s;" % (author,)
  mycursor.execute(sql)

  result = mycursor.fetchall() #should give UserID, SheetID

  if len(result) >0:
    #Has a active char already
    sql = "UPDATE users SET sheetID = %s WHERE userID = %s;" % (link ,author)
    mycursor.execute(sql)

  else:
    #has no active char
    sql = "INSERT INTO users (userID, sheetID) VALUES (%s, %s)"
    val = (author, link,)
    mycursor.execute(sql, val)

  return getCharacter(author, link)

def getCharacter(author, link):
  # Wix,
  # Standard Level Hero
  # Max Speed: 1000 kmh (Running)
  # Max Carry/Push: 1 tonne
  #
  # Attacks:
  # Unarmed 10d6
  # Strike 90d6
  body = "Test"

  return ["Posted!", body, "`$import`"]