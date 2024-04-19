import openai
import os
from dotenv import find_dotenv, load_dotenv
import json
import re
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from contextlib import nullcontext
from openai import OpenAI, AssistantEventHandler

########  GENERAL APP INFORMATION  ##############

APP_TITLE = "AI Debate Partner"
APP_INTRO = """
In this interactive exercise, you will participate in a structured debate with an AI, which challenges your reasoning and enhances your argumentative skills across various topics. After choosing a topic and a position to take, you'll engage in three rounds of debate, responding to the AI's prompts and refining your arguments. The exercise concludes with a summary from the AI, highlighting key points and providing feedback on your strengths and areas for improvement. Get ready to critically engage and articulate your thoughts in this casual virtual debate setting.
"""

APP_HOW_IT_WORKS = """
 **AI Debate Partner** is an interactive tool that facilitates structured debates between a student and an AI. Utilizing the OpenAI Assistants API with GPT-4, this tool is designed to simulate a real debate environment, allowing students to practice and refine their argumentative skills. Here’s how it works:

1. **Initiate the Debate:** Students can choose a topic they are interested in and input their initial stance on the issue. This kicks off the debate.
2. **Engage in Structured Rounds:** The AI begins the debate with a well-formed argument, setting the tone for a structured exchange. Students respond, and the AI analyzes these responses to present counterarguments. This cycle continues for three rounds, ensuring a comprehensive debate on the topic.
3. **Summary and Feedback:** After the debate rounds, the AI summarizes the discussion, highlighting key points and commendations for the student’s arguments. This helps students understand the strengths of their arguments and areas for improvement.

The tool is built to be an educational aid, encouraging students to think critically and articulate their thoughts clearly. It simulates a learning environment where students can freely experiment with ideas and receive immediate, constructive feedback.

Key Features and Considerations:

- **Feedback and Learning:** The AI provides ongoing feedback throughout the debate, helping students to refine their arguments and consider new perspectives.
- **Experimental Scoring:** While there is no numerical scoring, the AI’s feedback acts as a qualitative assessment of the student’s performance, focusing on the depth and relevance of their arguments rather than on a point system.
- **AI Limitations:** As with any AI-driven tool, the responses are generated based on patterns in data and may not always perfectly align with human reasoning. Students are encouraged to use critical thinking to assess the AI’s feedback and consider its relevance to their arguments.
- **Educational Focus:** The primary aim is to enhance educational experiences, not to replace traditional learning methods. The tool serves as a complement to classroom learning, providing a safe space for students to practice and improve their debate skills.
 """

SHARED_ASSET = ""

COMPLETION_MESSAGE = "You've reached the end! I hope you learned something!"
COMPLETION_CELEBRATION = False

SCORING_DEBUG_MODE = True

 ####### PHASES INFORMATION #########

PHASES = {
    "welcome": {
        "type": "markdown",
        "body": """<h2>Welcome to the Debate Portal! </h2> <p>You'll start by providing your name and a topic you'd like to debate.</p>""",
        "unsafe_allow_html": True,
        "no_submission": True
    },
    "user_name": {
        "type": "text_input",
        "label": """What is your name?""",
        "instructions": """The user will provide you their name. In one sentence only, welcome them by name and end your statement with 'Let's try a friendly debate in order to increase your understanding and fluency in the topic.'""",
        "allow_skip": False,
        "scored": False,
    },
    "debate_topic": {
        "type": "selectbox",
        "label": "Choose a debate topic (Round 1)",
        "options": ['Telemedicine: I believe that the rise in telemedicine will improve health outcomes.', 'Telemedicine: I believe that the rise in telemedicine will harm health outcomes.', 'Wearables: I believe the benefits of wearable health technologies outweigh the risk of data breaches', 'Wearables: I believe the risk of data breaches outweigh the benefits of wearable health technologies.', 'Health Data Ownership: I believe that patients should have autonomy and privacy over their personal information.', 'Health Data Ownership: I believe that health information can be shared in order to improve individual and public health outcomes.'],
        "placeholder": "Select debate topic",
        "allow_skip": False,
        "instructions": """The user will provide you a topic and their stance on the topic. Take the opposite stance, and generate an introductory statement for the debate. Ensure your statement is clear, evidence-based, and structured to provoke thoughtful discourse. End your statement with 'Why did you choose the stance you chose?'""",
    },
    "round_1": {
        "type": "text_area",
        "height": 300,
        "label": """Outline Your Position (Round 2)""",
        "instructions": """The user will respond to your opening statement. Respond to the student's argument by addressing their points and introducing new evidence or perspectives on the topic. Aim to challenge the student's stance constructively.""",
        "value": """The rise in telemedicine is poised to significantly improve health outcomes for several reasons. First, it greatly increases accessibility to healthcare, especially for individuals in remote or underserved areas who might otherwise face significant barriers to accessing medical services. By enabling patients to consult with doctors via video or phone, telemedicine reduces travel time and associated costs, making it easier for patients to seek care promptly. Secondly, telemedicine supports the continuous monitoring of chronic conditions, allowing for timely adjustments in treatment and preventing complications. This proactive approach can lead to better overall management of chronic diseases and improved long-term health outcomes. Additionally, telemedicine can alleviate the strain on overburdened healthcare facilities by handling routine consultations online, thus improving the quality and speed of both virtual and in-person care services. Overall, the integration of telemedicine into healthcare systems promises a more accessible, efficient, and patient-centered approach to medical care, leading to enhanced health outcomes.""",
        "scored": False,
        "allow_skip": False,
        "user_input": "",
    },
    "round_2": {
        "type": "text_area",
        "height": 300,
        "label": """Respond and Defend your Position (Round 3)""",
        "instructions": """Summarize the key points of the debate, highlighting the student's strong arguments and commend them for their insights. Conclude the debate by reiterating the importance of discussing such topics.""",
        "button_label": "Submit",
        "value": """
Addressing the challenges presented by the rise of telemedicine requires a multifaceted approach to ensure that its benefits are maximized without exacerbating disparities or compromising care quality:

Enhance Digital Literacy: Implementing educational programs tailored for elderly patients and those unfamiliar with technology can help bridge the technology gap. Healthcare providers can partner with community centers and libraries to offer training sessions on using telehealth platforms effectively.
Improve Technology Access: Governments and healthcare organizations should work together to provide subsidized or free devices and internet services to low-income or technologically underserved populations. This can help ensure that everyone has the necessary tools to benefit from telemedicine.
Hybrid Models of Care: Develop models of care that combine telemedicine with traditional in-person visits. For example, routine follow-ups and monitoring could be conducted virtually, while ensuring easy and quick access to in-person care when a physical examination is necessary.
Standardize Telemedicine Practices: Establish clear guidelines and standards for telemedicine practices to ensure consistent quality across services. This includes protocols for when to refer patients for in-person care and how to conduct thorough virtual assessments.
Incorporate Remote Monitoring Tools: Utilize advanced remote monitoring technologies that can provide more comprehensive data to healthcare providers. Devices that measure vital signs, blood sugar levels, and other important health metrics can provide data that enhances the quality of virtual consultations.
Regular Quality Assessments and Feedback Mechanisms: Regularly assess the quality of telemedicine services and gather patient feedback to continuously improve the system. This can help identify areas where telemedicine is failing and areas where it excels, allowing for targeted improvements.
By tackling these challenges through strategic initiatives and policies, the potential of telemedicine to enhance healthcare accessibility and effectiveness can be fully realized without sacrificing the quality of care.""",
        "scored_phase": False,
        "rubric": "",
        "minimum_score": 0,
        "allow_skip": False,
        "user_input": "",
    },
}

######## AI CONFIGURATION #############
OPENAI_MODEL = "gpt-4-turbo"
ASSISTANT_ID = "asst_SLSuT2rtar3Aalu0qUPfqTnf"
ASSISTANT_THREAD = ""
FREQUENCY_PENALTY = 0
MAX_TOKENS = 1000
PRESENCE_PENALTY = 0
TEMPERATURE = 1
TOP_P = 1

########## AI ASSISTANT CONFIGURATION #######
ASSISTANT_NAME = "Debate Partner"
ASSISTANT_INSTRUCTIONS = """
You are a debate partner for a university-level student taking a course about the debate topic. You will take a side of your choosing or provided by the student on a topic. You will present your arguments convincingly and with evidence. You also recognize clear and evidence-based arguments put forward by the student. """


load_dotenv()
client = openai.OpenAI()

function_map = {
    "text_input": st.text_input,
    "text_area": st.text_area,
    "warning": st.warning,
    "button": st.button,
    "radio": st.radio,
    "markdown": st.markdown,
    "selectbox": st.selectbox
}

user_input = {}

def build_field(i, phases_dict):

    phase_name = list(phases_dict.keys())[i]
    phase_dict = list(phases_dict.values())[i]
    field_type = phase_dict.get("type","")
    field_label = phase_dict.get("label","")
    field_body = phase_dict.get("body","")
    field_value = phase_dict.get("value","")
    field_max_chars = phase_dict.get("max_chars",None)
    field_help = phase_dict.get("help","")
    field_on_click = phase_dict.get("on_click",None)
    field_options = phase_dict.get("options",[])
    field_horizontal = phase_dict.get("horizontal",False)
    field_height = phase_dict.get("height",None)
    field_unsafe_html = phase_dict.get("unsafe_allow_html", False)
    field_placeholder = phase_dict.get("placeholder","")

    kwargs = {}
    if field_label:
        kwargs['label'] = field_label
    if field_body:
        kwargs['body'] = field_body
    if field_value:
        kwargs['value'] = field_value
    if field_options:
        kwargs['options'] = field_options
    if field_max_chars:
        kwargs['max_chars'] = field_max_chars
    if field_help:
        kwargs['help'] = field_help
    if field_on_click:
        kwargs['on_click'] = field_on_click
    if field_horizontal:
        kwargs['horizontal'] = field_horizontal
    if field_height:
        kwargs['height'] = field_height
    if field_unsafe_html:
        kwargs['unsafe_allow_html'] = field_unsafe_html
    if field_placeholder:
        kwargs['placeholder'] = field_placeholder
 
    key = f"{phase_name}_phase_status"
    
    #If the user has already answered this question:
    if key in st.session_state and st.session_state[key]:
        #Write their answer
        if f"{phase_name}_user_input" in st.session_state:
            if field_type != "selectbox":
                kwargs['value'] = st.session_state[f"{phase_name}_user_input"]
            kwargs['disabled'] = True
        

    my_input_function = function_map[field_type]

    with stylable_container(
        key="large_label",
        css_styles="""
            label p {
                font-weight: bold;
                font-size: 28px;
            }
            """,
    ):

        user_input[phase_name] = my_input_function(**kwargs)


class AssistantManager:
    assistant_id = ASSISTANT_ID
    thread_id = ASSISTANT_THREAD
    
    def __init__(self, model: str = OPENAI_MODEL):
        self.client = client
        self.model = OPENAI_MODEL
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        # Retrieve existing assistant and thread if IDs are already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name, instructions=instructions, tools=tools, model=self.model
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"AssisID:::: {self.assistant.id}")

    def create_thread(self):
        if not self.thread:
            print(st.session_state['thread_obj'])
            if st.session_state.thread_obj:
                print(f"Grabbing existing thread...")
                thread_obj = st.session_state.thread_obj
            else:
                print(f"Creating and saving new thread")
                thread_obj = self.client.beta.threads.create()
                st.session_state.thread_obj = thread_obj

            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"ThreadID::: {self.thread.id}")
        else:
            print(f"A thread already exists: {self.thread.id}")

    # Create a MESSAGE within our thread. Indicate if the message is from the user or assistant.
    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, 
                role=role, 
                content=content
            )

    # Create a RUN that sends the thread (with our messages) to the ASSISTANT
    def run_assistant(self, instructions, current_phase, scoring_run=False, temperature = TEMPERATURE, response_format="auto"):
        if self.thread and self.assistant:

            # Create a RUN that sends the thread (with our messages) to the ASSISTANT
            if not scoring_run or (scoring_run and SCORING_DEBUG_MODE):
                res_box = st.info(body="", icon="🤖")
            report = []

            stream = self.client.beta.threads.runs.create(
                assistant_id=self.assistant.id,
                thread_id=self.thread.id,
                instructions=instructions,
                temperature=temperature,
                stream=True
                )

            context_manager = st.spinner('Checking Score...') if scoring_run else nullcontext()

            with context_manager:
                for event in stream:
                    if event.data.object == "thread.message.delta":
                        #Iterate over content in the delta
                        for content in event.data.delta.content:
                            if content.type == 'text':
                                #Print the value field from text deltas
                                report.append(content.text.value)
                                result = "".join(report).strip()
                                if scoring_run == False:
                                    res_box.info(body=f'{result}', icon="🤖")
                                if scoring_run and SCORING_DEBUG_MODE:
                                    res_box.info(body=f'SCORE (DEBUG MODE): {result}', icon="🤖")


            if scoring_run == False:
                st_store(result,current_phase,"ai_response")
            else:
                st_store(result,current_phase,"ai_result")
                score = extract_score(result)
                st_store(score,current_phase,"ai_score")




def st_store(input, phase_name, phase_key):
    key = f"{phase_name}_{phase_key}"
    if key not in st.session_state:
        st.session_state[key] = input
        

def build_scoring_instructions(rubric):
    scoring_instructions = """Please score the user's previous response based on the following rubric: \n """
    scoring_instructions += rubric
    scoring_instructions += """\n\nPlease output your response as JSON, using this format: { "[criteria 1]": "[score 1]", "[criteria 2]": "[score 2]", "total": "[total score]" }"""
    return scoring_instructions

def extract_score(text):
    # Define the regular expression pattern
    #regex has been modified to grab the total value whether or not it is returned inside double quotes. The AI seems to fluctuate between using quotes around values and not. 
    pattern = r'"total":\s*"?(\d+)"?'
    
    # Use regex to find the score pattern in the text
    match = re.search(pattern, text)
    
    # If a match is found, return the score, otherwise return None
    if match:
        return int(match.group(1))
    else:
        return 0


def check_score(PHASE_NAME):
    score = st.session_state[f"{PHASE_NAME}_ai_score"]
    try:
        if score >= PHASES[PHASE_NAME]["minimum_score"]:
            st.session_state[f"{PHASE_NAME}_phase_status"] = True
            return True
        else:
            st.session_state[f"{PHASE_NAME}_phase_status"] = False
            return False
    except:
        st.session_state[f"{PHASE_NAME}_phase_status"] = False
        return False

def skip_phase(PHASE_NAME, No_Submit=False):
    st_store(user_input[PHASE_NAME], PHASE_NAME, "user_input")
    if No_Submit == False:
        st.session_state[f"{PHASE_NAME}_ai_response"] = "This phase was skipped."
    st.session_state[f"{PHASE_NAME}_phase_status"] = True
    st.session_state['CURRENT_PHASE'] = min(st.session_state['CURRENT_PHASE'] + 1, len(PHASES)-1)


def celebration():
    rain(
        emoji="🥳",
        font_size=54,
        falling_speed=5,
        animation_length=1,
    )



def main():
    global ASSISTANT_ID

    if 'CURRENT_PHASE' not in st.session_state:
        st.session_state.thread_obj = []

    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    if APP_HOW_IT_WORKS:
        with st.expander("Learn how this works", expanded=False):
            st.markdown(APP_HOW_IT_WORKS)


    if SHARED_ASSET:
        # Download button for the PDF
        with open(SHARED_ASSET["path"], "rb") as asset_file:
            st.download_button(label=SHARED_ASSET["button_text"],
                data=asset_file,
                file_name=SHARED_ASSET["name"],
                mime="application/octet-stream")

    #Create the assistant one time. Only if the Assistant ID is not found, create a new one. 
    openai_assistant = AssistantManager()
    
    #Run the create_assistant. It only creates a new assistant if one is not found. 
    openai_assistant.create_assistant(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        tools=""
    )

    #Create a thread, or retrieve the existing thread if it exists in local Storage. 
    openai_assistant.create_thread()
    
    i=0

    #Create a variable for the current phase, starting at 0
    if 'CURRENT_PHASE' not in st.session_state:
        st.session_state['CURRENT_PHASE'] = 0


    #Loop until you reach the currently active phase. 
    while  i <= st.session_state['CURRENT_PHASE']:
        submit_button = False
        skip_button = False
        final_phase_name = list(PHASES.keys())[-1]
        final_key = f"{final_phase_name}_ai_response"



        # Build the field, according to the values in the PHASES dictionary
        build_field(i, PHASES)
        #Store the Name of the Phase and the values for that Phase
        PHASE_NAME = list(PHASES.keys())[i]
        PHASE_DICT = list(PHASES.values())[i]

        key = f"{PHASE_NAME}_phase_status"
      
        #Check phase status to automatically continue if it's a markdown phase
        if PHASE_DICT["type"] == "markdown":
            if key not in st.session_state:
                st.session_state[key] = True
                st.session_state['CURRENT_PHASE'] = min(st.session_state['CURRENT_PHASE'] + 1, len(PHASES) - 1)

        
        if key not in st.session_state:
            st.session_state[key] = False
        #If the phase isn't passed and it isn't a recap of the final phase, then give the user a submit button
        if st.session_state[key] != True and final_key not in st.session_state:
            with st.container(border=False):
                col1, col2 = st.columns(2)
                with col1:
                    submit_button = st.button(label=PHASE_DICT.get("button_label","Submit"), type="primary", key="submit "+str(i))
                with col2:
                    if PHASE_DICT.get("allow_skip", False):
                        skip_button = st.button(label="Skip Question", key="skip " + str(i))

        #If the phase has user input:
        key = f"{PHASE_NAME}_user_input"
        if key in st.session_state:
            # Then try to print the stored AI Response
            key = f"{PHASE_NAME}_ai_response"
            #If the AI has responded:
            if key in st.session_state:
                #Then print the stored AI Response
                st.info(st.session_state[key], icon ="🤖")
            key = f"{PHASE_NAME}_ai_result"
            #If we are showing a score:
            if key in st.session_state and SCORING_DEBUG_MODE == True:
                #Then print the stored AI Response
                st.info(st.session_state[key], icon ="🤖")

        if submit_button:
            #Add INSTRUCTIONS message to the thread
            openai_assistant.add_message_to_thread(
                role="assistant", 
                content=PHASE_DICT.get("instructions","")
                )
            #Store the users input in a session variable
            st_store(user_input[PHASE_NAME], PHASE_NAME, "user_input")
            #Add USER MESSAGE to the thread
            openai_assistant.add_message_to_thread(
                role="user", 
                content=user_input[PHASE_NAME]
                )
            #Currently, all instructions are handled in the system prompts, so no need to add additional instructions here. 
            instructions = ""
            #Run the thread
            openai_assistant.run_assistant(instructions, PHASE_NAME)
            
            if PHASE_DICT.get("scored_phase","") == True:
                if "rubric" in PHASE_DICT:
                    scoring_instructions = build_scoring_instructions(PHASE_DICT["rubric"])
                    openai_assistant.add_message_to_thread(
                    role="assistant", 
                    content=scoring_instructions,
                    )
                    openai_assistant.run_assistant(instructions, PHASE_NAME, True, temperature=.2,response_format="json")
                    if check_score(PHASE_NAME):
                        st.session_state['CURRENT_PHASE'] = min(st.session_state['CURRENT_PHASE'] + 1, len(PHASES)-1)
                    else:
                        st.warning("You haven't passed. Please try again.")
                else:
                    st.error('You need to include a rubric for a scored phase', icon="🚨")
            else: 
                st.session_state[f"{PHASE_NAME}_phase_status"] = True
                st.session_state['CURRENT_PHASE'] = min(st.session_state['CURRENT_PHASE'] + 1, len(PHASES)-1)

            #Rerun Streamlit to refresh the page
            st.rerun()

        if skip_button:
            skip_phase(PHASE_NAME)
            st.rerun()


        if final_key in st.session_state and i == st.session_state['CURRENT_PHASE']:
            st.success(COMPLETION_MESSAGE)
            if COMPLETION_CELEBRATION:
                celebration()

        #Increment i, but never more than the number of possible phases
        i = min(i + 1, len(PHASES))




if __name__ == "__main__":
    main()