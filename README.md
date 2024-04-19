# AI MicroApp (Assistants)

## Overview
This AI MicroApp template is a simple Streamlit application that demonstrates how to integrate AI models with a web interface using Streamlit. It means that you can build and share AI "MicroApps" as simply as building a form. 

It works with the OpenAI Assistants API and similar. With the Assistants API, there is "memory" of a conversation and the AI and the user go back and forth in a conversation. Each round of conversation is called a "phase". It is most suitable an AI giving feedback or a short conversation with a user. For example, exercises like "Provide feedback for one or more drafts of an excerpt", or "Have a debate with AI". 

It also doesn't store data anywhere except for some storage required in the local browser which is cleared after the session ends. The conversation is sent to the AI and stored according to that specific AI's policies. 

## Prerequisites
- Python 3.6 or later
- pip
- virtualenv (optional but recommended)
- OpenAI, Claude, and/or Google Gemini API key(s)

## Local Setup Instructions

### 1. Clone the repository

Navigate to a location where you'd like to run this app from, and clone the repo:

```bash
git clone https://github.com/jswope00/AI-MicroApp-Template-Assistants.git
```

### 2. Create a Virtual Environment

To create a virtual environment, navigate to your project directory in the terminal:
```bash
cd AI-MicroApp-Template-Assistants
```

It's recommended to isolate the project's dependencies using a virtual environment. You can utilize tools like venv or virtualenv to achieve this. Refer to official documentation for specific commands based on your chosen tool. Here is the command from a mac shell:
```bash
python3 -m venv venv
```

Finally, activate your virtual environment:
```bash
source venv/bin/activate
```

### 3. Install Requirements
Activate your virtual environment and install the required packages using pip:
```bash
pip3 install -r requirements.txt
```

### 3. Add your API key(s):
Create a file named .env in your project's root directory. Paste your API key(s) inside the file. See .env_sample file for required format. 

## Running the App

### 1. Start the app

Navigate to your project directory in the terminal and execute the following command to launch the Streamlit app:
```bash
streamlit run main.py
```

This will open the Birthday App in your web browser, typically at http://localhost:8501.


### Explanation

The app leverages Streamlit to create a user interface and OpenAI's API for interacting with a large language model. Here's a breakdown of the key functionalities:

-   **User Input:**  The app gathers user information through text input fields and radio buttons for name, age, and birth month.
-   **Prompt Building:**  The app constructs prompts for the AI based on the user's input and manages the "phases" or conversation turns between AI and user, allowing for dynamic interaction.
-   **Scoring:** Optionally, phases can be scored. Scoring is performed by the AI based on a phase-specific rubric. Scoring is experimental. Scoring must use GPT-4 (ChatGPT3.5 is not smart enough), and it is not recommended to show scores to users. At this point, best practice is to use rubrics to determine a "good faith effort" and always allow users to skip a question if the scoring system behaves unexpectedly.
-   **API Interaction:**  The app sends the constructed prompt to the OpenAI API using your provided key and retrieves the response.
-   **Output:**  The AI's response is displayed within the Streamlit app.

### Customization

The code includes sections for various app aspects you can customize:

-   `APP_TITLE`: Update the application title displayed at the top.
-   `APP_INTRO`: Modify the introductory text providing a brief description of the app.
-   `APP_HOW_IT_WORKS`: (Optional) Include a detailed explanation of the app's functionality within an expandable section.
-   `SHARED_ASSET`: (Optional) If you have an asset (like a PDF) to share, configure its download button here.
- 	`SCORING_DEBUG_MODE`: Setting to true will show the scores received from the AI for scored phases
-   `PHASES`: A dictionary of values that dictate phase fields and prompts. More documentation is required here, but the keys for field arguments generally map to Streamlit's documentation
-   `AI_CONFIGURATION`: This section configures various parameters for the OpenAI API call, such as the model to use, temperature, and token limits.

Feel free to experiment with these configurations to tailor the app's behavior and appearance to your preferences.


