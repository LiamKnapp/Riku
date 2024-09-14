import re, user_query, logging
from Chatbot import ai
from ImageBot import stablediffusion

# Alpha 1.0
#TODO Decide on the voice of the AI to use
#TODO Fine-tune the AI for personality
#TODO Option to switch between different LLM models that can be trained for different specific things

# Alpha 1.5
#TODO create a control pannel UI (website ran locally? application?) that allows for (skipping the ai's dialog, muting the speech to text whisper ai, saveing the short term memory, stopping the application, visulization of what the ai looks like, chat box of all messages being sent and recieved)
#TODO improve the saving short term memory, possible methods include writeing the context to the json after each item is appended into it rather then all at once when closeing the app.
#TODO for long responses and prompts being saved into the memory, make a "summarized" version of the response & prompt so that the short term memory can hold more data and less storage drain
#TODO Make long term data storage (Vector Database)

# Alpha 2.0
#TODO Ai plays Osu!
#TODO Ai plays D&D
#TODO Ai plays Diffuse the bomb (Keep Talking and Nobody .Explodes)
#TODO Ai gets computer vision


# Exiting the application with context saving
def exit_application():
    exit()

def model_controller(user_prompt): # Control what model to use depending on the prompt
    # Define the regular expression pattern
    pattern = r"(Generate me an image|Make me an image|Generate me a Photo|Make me a photo|Can you draw me)"
    # Search for the pattern in the text
    match = re.search(pattern, user_prompt, re.IGNORECASE)
    if bool(match) == True:
        stablediffusion.Generate_Image(user_prompt) # Generate the Ai's image to the users query
    else:
        ai.generate_response(user_prompt, engine)  # Generate the Ai's response to the users query

def main():
    # Handling KeyboardInterrupt to exit the applications
    try:
        while True:
                user_prompt = user_query.Get_Speech()  # Get the users prompt via speech to text
                model_controller(user_prompt) # Determine what AI model to use depending on the prompt
    except KeyboardInterrupt: # Close the app and save the context of the short-term memory in a json file
        print("\nKeyboard Interruption Exiting...\n")
        ai.save_context()

if __name__ == '__main__':
    from RealtimeTTS import CoquiEngine
    logging.basicConfig(level=logging.INFO)    
    engine = CoquiEngine(voice="./models/v2.0.2/snoop_dogg.wav", level=logging.WARNING, speed=1.25)
    ai.restore_context()
    main()