#1. Why did you choose to test the code that you did?

I tested my bot commands in the unmocked test file, I tested every single command and empty messages to make sure they properly work

In the mocked test file, I tested every socketio event function, but did not test any database functionality, instead I mocked those 
functions to return their respective objects. Also in the mocked test files I tested my bot commands that required API requests 
with all expected answers from the respective APIs. 


#2. Is there anything else you would like to test if you had the time

I would have liked to test the database functions and learn how to properly mock it but I did not have time.
