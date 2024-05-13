import ollama, time, keyboard, json, app
from datetime import datetime
from RealtimeTTS import TextToAudioStream

MAX_Memory = 1000 # specify the limit of the short term memory capacity
context = [] # Saves the response of the users speech and the ais responses
context_file_path = "./Chatbot/llm_ShortTermMemory.json"
AiModel = "llama3" # Define the Ai model to be used

# Function to save context to a JSON file
def save_context_to_json(context):
    with open(context_file_path, 'w') as json_file:
        json.dump(context, json_file)
    app.exit_application()

def is_last_role_assistant():
    if context:  # Check if context is not empty
        last_item = context[-1]  # Get the last item in the context
        if "role" in last_item and last_item["role"] == "assistant":
            context.pop() # remove the last ai's response as the generation was stopped and should not be saved
            context.pop() # remove the users prompt as the ai never makes a response to the prompt
        elif  "role" in last_item and last_item["role"] == "user":
            context.pop() # remove the users prompt as the ai never makes a response to the prompt

def add_item_to_list(item, context): # ensure that the conext memory does not exceed the upper limit.
    if len(context) < MAX_Memory: # increaseing the max memory will allow for holding more context
        context.append(item)
    else:
        context.pop() # remove the last user prompt
        context.pop() # remove the ai's response associated with that users prompt
        context.append(item)

def restore_context():
    global context  # Declare context as a global variable to modify it within the function
    try:
        with open(context_file_path, 'r') as file:
            file_content = file.read()
            if file_content.strip():  # Check if the file is not empty or contains only whitespace
                context = json.loads(file_content)
                current_dateTime = datetime.now()
                current_dateTime_str = current_dateTime.strftime(" (%Y-%m-%d, %H:%M:%S)") # Convert the datetime object to a string in a specific format 
                system_message = ({"role": "assistant", "content": "System booted at" + current_dateTime_str}) # Store the users speech prompt in the context and the timestamp
                add_item_to_list(system_message, context) # ensure the list is not at full capacity
                print("System Booted: Context loaded")
            else:
                print("System Booted: Context file is empty. Starting with an empty context.")
                context = []
    except FileNotFoundError:
        print("System Booted: No context file found. Starting with an empty context.")
        context = []
    except json.decoder.JSONDecodeError:
        print("System Booted: Error decoding JSON in context file. Starting with an empty context.")
        context = []

def save_context(): # close the app and save the context of the short term memory
    if context == "":
        exit()
    else:
        current_dateTime = datetime.now()
        current_dateTime_str = current_dateTime.strftime(" (%Y-%m-%d %H:%M:%S)") # Convert the datetime object to a string in a specific format 
        system_message = ({"role": "user", "content": "System shut off at" + current_dateTime_str}) # Store the users speech prompt in the context and the timestamp
        add_item_to_list(system_message, context) # ensure the list is not at full capacity
        save_context_to_json(context)

def chatbot(prompt: str):
    response = "" # empty string to hold the response
    for chunk in ollama.chat(model=AiModel, messages=prompt, stream=True): # send the prompt and get the generated text in real time
        if (text_chunk := chunk['message']['content']) is not None: 
            print(text_chunk, end='', flush=True) # Print the text as it arrives in real time
            response += text_chunk # Concatenate the response into the string
            yield text_chunk
    Ai_response = ({'role': 'assistant', 'content': response}) # Store the Ai's response in the context
    add_item_to_list(Ai_response, context)

def generate_response(prompt, TTSEngine):
        current_dateTime = datetime.now()
        current_dateTime_str = current_dateTime.strftime(" (%Y-%m-%d %H:%M:%S)") # Convert the datetime object to a string in a specific format 
        user_prompt = ({"role": "user", "content": prompt + current_dateTime_str}) # Store the users speech prompt in the context and the timestamp
        add_item_to_list(user_prompt, context) # ensure the list is not at full capacity
        stream = TextToAudioStream(TTSEngine).feed(chatbot(context[-MAX_Memory:])) # prompt the ai and play the prompt using text to speech
        stream.play_async(fast_sentence_fragment=True, buffer_threshold_seconds=999, minimum_sentence_length=18,) # play the text to speech in a seprate thread 
        print("\nPress '.' to stop the audio playback And not save the result!")
        print("Press ''' to stop the audio playback and save the result!")
        print("Press '/' to pause the audio playback!")
        print("Press ';' to resume the audio playback!")
        while stream.is_playing():
            if keyboard.is_pressed("."): # check if the user wants to stop the audio playback And not save the result
                stream.stop()
                is_last_role_assistant()
            if keyboard.is_pressed("'"): # check if the user wants to stop the audio playback and save the result
                stream.stop()
            if keyboard.is_pressed("/"): # check if the user wants to pause the audio playback
                stream.pause()
            if keyboard.is_pressed(";"): # check if the user wants to resume the audio playback
                stream.resume()
            time.sleep(0.1)