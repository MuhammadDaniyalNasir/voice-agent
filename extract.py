import subprocess

# Function to send a prompt to the Ollama model and return the response
# Uses subprocess to run the 'ollama' command-line tool
# prompt: The text prompt to send to the model
# model: The model name to use (default is 'llama3.1:latest')
def query_ollama(prompt, model = "gemma2:2b"):
    result = subprocess.run(
        ["ollama", "run", model],
        input = prompt.encode(),  # Pass the prompt as bytes to stdin
        capture_output = True     # Capture stdout and stderr
    )
    return result.stdout.decode()  # Return the decoded output from the model

# Helper function to extract a section of text between two keys
# text: The full text to search
# start_key: The string marking the start of the section
# end_key: The string marking the end of the section (optional)
def extract_section(text, start_key, end_key = None):
    """Helper function to safely extract text between two keys."""

    try:
        # Find the start index after the start_key
        start_index = text.index(start_key) + len(start_key)

        if end_key:
            # If end_key is provided, find the end index after start_index
            end_index = text.index(end_key, start_index)
            return text[start_index:end_index].strip()  # Return the section between keys

        return text[start_index:].strip()  # If no end_key, return from start_key to end
    
    except ValueError:
        # If start_key or end_key not found, return a message
        return f"{start_key.strip()} section not found."

# Main function to extract meeting data from a transcript
# transcript: The meeting transcript as a string
def extract_meeting_data(transcript):
    # Construct the prompt for the LLM, instructing it to extract decisions, action items, and a follow-up email
    prompt = f"""
You are a helpful assistant analyzing a meeting transcript.

From the transcript below, extract and clearly label the following sections using these exact headers — Summarize:, Decisions:, Action items:, and Follow-up:.

Format:

Summarize:
- Summary point 1
- Summary point 2

Decisions:
- Decision 1
- Decision 2

Action items:
- Task 1 by Person A
- Task 2 by Person B

Follow-up:
<Professional email summarizing the meeting>

Transcript:
{transcript}
"""


    # Get the response from the LLM
    response = query_ollama(prompt)
    print("RAW OLLAMA RESPONSE:\n", response)
    # Extract each section from the response using the helper function
    return {
        "summary": extract_section(response, "Summarize:", "Decisions:"),
        "decisions": extract_section(response, "Decisions:", "Action items:"),
        "action_items": extract_section(response, "Action items:", "Follow-up:"),
        "follow_up_email": extract_section(response, "Follow-up:")
    }

    