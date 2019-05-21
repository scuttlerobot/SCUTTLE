# Please run "sudo apt-get install festival" before running this program.
# Next, run the command: 'sudo amixer cset numid=1 100%' 
# this will raise the volume of your Pi audio output to 100%

import os

def say(s):

    s = str(s)  # Make sure input is a string by casting all inputs to a string.

    os.system("echo \"" + text + "\" | festival --tts")
    # Basically running a system command to perform text to speech
    # Running the command: echo "Hello, David." | festival --tts &

    # echo print the following text to the terminal

    # "|" takes the output from the last program (echo) that would have
    # gone to the terminal and sends it to the program specified (festival)
    # In linux this is called a "pipe".

    # "&" sends the program (festival) to the background immediately so the code
    # can move on without having to wait for the text to speech to complete
    # "festival" will die in the background once it is done.

text = "I am scuttle robot with 2 DC motors and 2.4gig-ahertz waifai \
as well as 5 gig-ahertz waifai. I have a maximum cruise velocity of 0.5 \
meters per second and my three cell lithium ion battery has 14 volts \
on a full charge."
say(text)
