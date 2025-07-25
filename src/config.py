# dict keys
GENERATED_POST = "generated_post"
TAGS = 'tags'
IMAGE_GENERATION_PROMPT = 'image_generation_prompt'

HISTORICAL_PERIODS = [
    "Prehistory",
    "Ancient History",
    "Classical Antiquity",
    "The Middle Ages",
    "The Renaissance",
    "The Age of Exploration",
    "The Reformation",
    "The Age of Enlightenment",
    "The Industrial Revolution",
    "The Napoleonic Era",
    "The Victorian Era",
    "The Gilded Age",
    "World War I",
    "The Interwar Period",
    "World War II",
    "The Cold War",
    "The Space Age",
    "The Information Age",
    "The Bronze Age",
    "The Iron Age",
    "The Roman Empire",
    "The Byzantine Empire",
    "The Islamic Golden Age",
    "The Viking Age",
    "The Edo Period (Japan)",
    "The Qing Dynasty (China)",
    "The British Empire",
    "The Belle Époque",
    "The Roaring Twenties",
    "The Digital Age"
]

AI_MODEL = "amazon.nova-lite-v1:0"

PROMPT_ROLE = "You are a Social Media Historian."
PROMPT_CONTEXT = """
Your audience is a general Facebook audience interested in surprising or significant moments from history, presented 
in an accessible and engaging way. The post needs to be concise (under 300 words) and end with five relevant hashtags. 
It should include some emojis.
"""
PROMPT_PERIOD_INSTRUCTION = "1. Choose a historical event from "
PROMPT_INSTRUCTIONS = """
2.  Briefly explain what happened, when, and where. Focus on the most compelling details.
3.  Highlight why is this event interesting or noteworthy.
4.  Include 5 relevant hashtags that summarize the content and encourage discoverability.
"""
PROMPT_OUTPUT_FORMAT = f"""
Output Format: Your response MUST be a valid JSON object with the following keys:
{{
  "{GENERATED_POST}": "Your engaging Facebook post text goes here (max 300 words).",,
  "{IMAGE_GENERATION_PROMPT}": "A detailed prompt for image generation AI related to the event."
}}
"""
TEMPERATURE = 0.9
MAX_TOKEN_COUNT = 500
STOP_SEQUENCES = []

AI_MODEL_REGION = "us-east-1"
DEFAULT_REGION = 'us-west-2'
GRAPH_API_VERSION = "v23.0"
