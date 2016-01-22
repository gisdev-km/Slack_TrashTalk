import mysql.connector
from .config import slackTeam, appSettings, mySQLSettings

class attachment(object):
    '''
        A class object for formatting attachments
    '''
    def __init__(self, text=None):
        self.fallback = ""
        self.color = "#ff0000"
        self.author = "trashtalk"
        self.text = text
        self.pretext = ""

def help():
    '''
        A function to return the limited commands available to the user
    '''

    response = """*{app}*\n
_Version_: {version}
_Source of Trash_: {burn}
\nTo use: /trashtalk @[user] to generate a random quote""".format(app=appSettings["app"].upper(), 
                                                                  version=appSettings["version"], 
                                                                  burn=appSettings["tt_url"])
    return response

def adminHelp():
    '''
        A function to return the limited admin commands available.
    '''

    response = """\n*TRASHTALK ADMIN COMMANDS*\n
_To add_: /trashtalk admin add [insult]
_To delete_: /trashtalk admin delete [insult id]
_To query for ID_: /trashtalk admin query [insult]
"""
    
    return response


def returnConn():
    '''
        A function to return a MySQL Connector object
    '''
    conn = mysql.connector.connect(user=mySQLSettings["user"], 
                                  password=mySQLSettings["password"], 
                                  host=mySQLSettings["host"], 
                                  database=mySQLSettings["database"])

    return conn

def getInsult():
    '''
        A function to return a random insult from the database
    '''
    conn = returnConn()
    cursor = conn.cursor()
    sql = "Select insult, id as oid from `Insults` JOIN (SELECT CEIL(RAND() * (SELECT MAX(id) FROM `Insults`)) as id) as r2 using (id);"
    cursor.execute(sql)
    results = cursor.fetchone()
    results = "{0}".format(results[0])
    conn.close()

    return results

def checkRecordID(id=None, insult=None):
    '''
        A function to obtain the ID of an insult either via ID or via insult string

        Note: Insult string must match exactly, does not support wild cards.
    '''
    conn = returnConn()
    cursor = conn.cursor()

    if not id == None:
        sql = "Select id from Insults where id = {0};".format(int(id))

    elif not insult == None:
        sql = "Select id from Insults where insult = '{0}';".format(insult)

    cursor.execute(sql)
    results = cursor.fetchone()

    return results

def addInsult(insult):
    '''
        A function to add insults to the database from within Slack
    '''
    results = checkRecordID(insult=insult)

    if results == None:
        conn = returnConn()
        cursor = conn.cursor()
        sql = "Insert into `Insults` (insult) Values ('{0}');".format(insult)
        cursor.execute(sql)
        newId = cursor.lastrowid
        conn.commit()
        response =  "*TRASHTALK ADMIN: SUCCESS* Insult added at record #{0}".format(newId)
    else:
        response = "*TRASHTALK ADMIN: ERR* Insult already exists at record #{0}".format(results[0])

    return response

def delInsult(insultID):
    '''
        A function to delete an insult from the database with the ID (int) of the insult.
    '''
    try:
        insultID = int(insultID)
        results = checkRecordID(id=insultID)

        if results == None:
            response = "*TRASHTALK ADMIN: ERR* Insult ID does not exist"
        else:
            conn = returnConn()
            cursor = conn.cursor()
            sql = "Delete from `Insults` where id = {0};".format(insultID)
            cursor.execute(sql)
            conn.commit()
            response = "*TRASHTALK ADMIN: SUCCESS* Insult ID #{0} has been deleted".format(insultID)
    except:
        response = "*TRASHTALK ADMIN: ERR* Insult ID is not an integer, aborting"

    return response

def queryInsult(insult):
    '''
        A function to query the database with the insult string to obtain the record ID
    '''

    results = checkRecordID(insult=insult)

    if not results == None:

        response = "*TRASHTALK ADMIN:* Insult Match at ID#{0}".format(results[0])

    else:
        response = "*TRASHTALK ADMIN:* No matching insult"

    return response