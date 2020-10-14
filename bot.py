import requests
import json
import json
import urllib.parse

def command(text):
    split_text = text.split(' ',2)
    
    if split_text[0] != "!!":
        return ""
    
    cmd = split_text[1]
    
    if cmd == "help":
        return "You can use these commands in the format '!! <command> <message>': about - help - funtranslate - 8ball - "
    
    elif cmd == "about":
        return "I'm a bot that answers to '!! <command> <message>'. Type '!! help' to learn more about commands"
    
    elif cmd == "funtranslate":
        payload = {'text' : split_text[2]}
        res = requests.get("https://api.funtranslations.com/translate/leetspeak.json", params = payload)
        return json.loads(res.text)['contents']['translated']
        
        
    elif cmd == "8ball":
        question = urllib.parse.quote(split_text[2])
        res = requests.get("https://8ball.delegator.com/magic/JSON/" + question)
        return json.loads(res.text)['magic']['answer']
        
    elif cmd == "TODO":
        return ""
    else:
        return "Command not recognized. Type '!! help' for list of commands"