import requests
import json
import random
import urllib.parse

def command(text):
    split_text = text.split(' ',2)
    
    if split_text[0] != "!!":
        return "Try using the form '!! command message'"
    
    cmd = split_text[1]
    
    if cmd == "help":
        return "You can use these commands in the format '!! command message'\
        :<br>about - About me!<br>help - This command<br>funtranslate - convert message to leetspeak<br>8ball - Ask a question to 8ball in your message<br>roll - roll a die from 1 to 6, you can set upper limit in message"
    
    elif cmd == "about":
        return "I'm a Leet Bot that answers to '!! command message'. Type '!! help' to learn more about commands"
        
    elif cmd == "funtranslate":
        payload = {'text' : split_text[2]}
        try: 
            res = requests.get("https://api.funtranslations.com/translate/leetspeak.json", params = payload)
        except KeyError: 
            return "I'm over my limit for this API call 😩"
        return json.loads(res.text)['contents']['translated']
        
        
    elif cmd == "8ball":
        question = urllib.parse.quote(split_text[2])
        try: 
            res = requests.get("https://8ball.delegator.com/magic/JSON/" + question)
        except KeyError: 
            return "I'm over my limit for this API call 😩"
        return json.loads(res.text)['magic']['answer']
        
    elif cmd == "roll":
        if(split_text[2]):
            try:
                upper_limit = int(split_text[2])
            except ValueError:
                return "Please enter a valid number. !! help to learn how to use this command"
            num = random.randint(1,int(split_text[2]))
        else:
            num = random.randint(1,6)
        return str(num)
        
    else:
        return "Command not recognized. Type '!! help' for list of commands"