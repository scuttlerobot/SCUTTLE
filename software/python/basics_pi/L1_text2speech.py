# Text to Speech program for SCUTTLE running RasPi
# Takes a message "s" and sends it as a voice to the audio output.
# Please run "sudo apt-get install festival" before running this program.
# Next, run the command: 'sudo amixer cset numid=1 100%'
# This will raise the volume of your Pi audio output to 100%

# Import external programs
import os # for making commands to festival program

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

if __name__ == "__main__":              # loop only executes if program is run directly (not imported)
    while 1:
        text = input("Enter text:")
        say(text)
