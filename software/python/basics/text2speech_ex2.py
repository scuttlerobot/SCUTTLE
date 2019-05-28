# Please run "sudo apt-get install festival"

import os

def say(s):

    s = str(s)  # Make sure input is a string by casting all inputs to a string.

    os.system("echo \"" + s + "\" | festival --tts")
    # Basically running a system command to perform text to speech
    # Running the command: echo "Hello, David." | festival --tts &

    # echo print the following text to the terminal

    # "|" takes the output from the last program (echo) that would have
    # gone to the terminal and sends it to the program specified (festival)
    # In linux this is called a "pipe".

    # "&" sends the program (festival) to the background immediately so the code
    # can move on without having to wait for the text to speech to complete
    # "festival" will die in the background once it is done.


# while 1:
#     text = input("Enter text:")
#     say(text)
