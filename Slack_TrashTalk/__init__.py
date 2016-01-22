from flask import Flask
from flask_slack import Slack

from .trashtalk import *
from .config import slackTeam, appSettings

app = Flask(__name__)
slack = Slack(app)

app.add_url_rule('/', view_func=slack.dispatch)

@slack.command(appSettings["command"], 
               token=slackTeam["token"], 
               team_id=slackTeam["id"], 
               methods=["POST"])

def trashTalk(**kwargs):

    text = kwargs.get("text")
    if " " in text:
        text = text.split(" ")
    else:
        text = [text]

    #print "Raw: {0}".format(text)

    response_type = 'ephemeral' 
    response_payload = help()
    attachments = []

    if len(text) > 0:
        if text[0].startswith("@"):
            
            text = text[0]

            response_type = 'in_channel'
        
            insult = getInsult()
        
            attachment = trashtalk.attachment()
            attachment.pretext = "Hey {0}...".format(text)
            attachment.fallback = "Hey {0}: {1}".format(text, insult)
            attachment.text = insult

            # Empty this out so the text in the attachment doesn't double-post
            response_payload = "" 
            attachments = [ attachment.__dict__]

        elif text[0].startswith("admin"):
        
            response_payload = adminHelp()

            for i, item in enumerate(text):
                text[i] = item.replace("'", "\'").replace('"', '\"')

            if len(text) > 2:

                if text[1].lower() == "add":
                    newInsult = " ".join(text[2:])
                    response_payload = addInsult(newInsult)

                elif text[1].lower() == "delete":
                    id = text[2]
                    response_payload = delInsult(id)
                elif text[1].lower() == "query":
                    insult = " ".join(text[2:])

                    response_payload = queryInsult(insult)

    return slack.response(response_payload, 
                          response_type=response_type, 
                          attachments=attachments)
