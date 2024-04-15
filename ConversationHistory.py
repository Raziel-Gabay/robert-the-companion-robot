import json

def save_log(request, response, filename='conversation_log.json'):
      # Load existing content if the file exists
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If the file is empty or doesn't exist, start with an empty list
        content = []

    # Append the new request and response as separate objects
    content.append(request)
    content.append(response)

    # Write the modified content back to the file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)

def load_log(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            if content:
                return json.loads(content)
            else:
                return []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def format_messages_for_api(conversation):
    formatted_messages = []
    for message in conversation:
        role = message["role"]
        content = message["content"]
        formatted_messages.append(f"{role}: {content}")

    return "\n".join(formatted_messages)

def add_message(request, response, conversation_history):
    conversation_history.append(request)
    conversation_history.append(response)
