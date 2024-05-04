import User_Query, re
from Chatbot import Ai
from ImageBot import StableDiffusion

#TODO Add model controller to swap between models depending on what you may need. (images, chat, games, etc...)
#TODO TRAIN/FINE TUNE THE AI 
#TODO improve the saving short term memory, possible methods include writeing the context to the json after each item is appended into it rather then all at once when closeing the app.
#TODO for long responses and prompts being saved into the memory, make a "summarized" version of the response & prompt so that the list can hold more data and less storage drain
#TODO research long term memory solutions (vector database)
#TODO create a control pannel UI (website ran locally? application?) that allows for (skipping the ai's dialog, muting the speech to text whisper ai, saveing the short term memory, stopping the application, visulization of what the ai looks like, chat box of all messages being sent and recieved)

# Exiting the application with context saving
def exit_application():
    exit()

def model_controller(user_prompt): # Control what model to use depending on the prompt
    # Define the regular expression pattern
    pattern = r"(Generate me an image|Make me an image|Generate me a Photo|Make me a photo|Can you draw me)"
    # Search for the pattern in the text
    match = re.search(pattern, user_prompt, re.IGNORECASE)
    if bool(match) == True:
        StableDiffusion.Generate_Image(user_prompt) # Generate the Ai's image to the users query
    else:
        Ai.generate_response(user_prompt)  # Generate the Ai's response to the users query

def main():
    # Handling KeyboardInterrupt to exit the applications
    try:
        while True:
                user_prompt = User_Query.Get_Speech()  # Get the users prompt via speech to text

                model_controller(user_prompt) # Determine what AI model to use depending on the prompt
    except KeyboardInterrupt: # Close the app and save the context of the short-term memory in a json file
        print("\nKeyboard Interruption Exiting...\n")
        Ai.save_context()

if __name__ == '__main__':
    Ai.restore_context()
    main()