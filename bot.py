import requests

def command(text):
    
    
    if text[:2] != "!!":
        return ""
        
    command = text.split()[1]
    
    if command == "help":
        return "You can use these commands :<br> help - <br>funtranslate - <br>8ball - <br>"
    
    if command == "about":
        return ""