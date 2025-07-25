# Keys for dictionaries used internally
GENERATED_POST = "generated_post"
TAGS = 'tags'
IMAGE_GENERATION_PROMPT = 'image_generation_prompt'

# List of historical periods for random selection
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
    "The Digital Age",
    "The Stone Age",
    "The Neolithic Revolution",
    "The Hellenistic Period",
    "The Early Middle Ages",
    "The High Middle Ages",
    "The Late Middle Ages",
    "The Baroque Period",
    "The Rococo Period",
    "The Age of Revolutions (18th-19th Century)",
    "The Great Depression",
    "The Post-War Boom (1945-1970s)",
    "The Counterculture Era",
    "The New Frontier (US)",
    "The Vietnam War Era",
    "The Silicon Age",
    "The Genomic Age",
    "The Anthropocene",
    "The Sumerian Civilization",
    "The Akkadian Empire",
    "The Babylonian Empire",
    "The Assyrian Empire",
    "The Republic of Rome",
    "The Holy Roman Empire",
    "The Mongol Empire",
    "The Ottoman Empire",
    "The Early Modern Period",
    "The Late Modern Period",
    "The Contemporary Period",
    "The Post-Cold War Era",
    "The War on Terror Era",
    "The Globalization Era",
    "The Rise of Islam",
    "The Crusades",
    "The Black Death Era",
    "The Columbian Exchange",
    "The Scientific Revolution",
    "The Age of Absolutism",
    "The Romantic Era",
    "The Age of Imperialism",
    "The Fin de Siècle",
    "The Space Race",
    "The Great Recession Era",
    "The Age of Social Media",
    "The Digital Revolution",
]

# --- AI Model Configuration for Text Generation (Bedrock) ---
AI_MODEL = "amazon.nova-lite-v1:0"
TEMPERATURE = 0.9 # Controls creativity/randomness (0.0-1.0)
MAX_TOKEN_COUNT = 500 # Maximum number of tokens the AI can generate in response
STOP_SEQUENCES = [] # List of strings that will cause the AI to stop generating text

# --- AWS Regions for Bedrock Services ---
AI_MODEL_REGION = "us-east-1" # Region where the primary text generation AI model is deployed
DEFAULT_REGION = 'us-west-2' # Default region, used for the image generation AI model

# --- Prompt Components for AI Text Generation ---
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
  "{GENERATED_POST}": "Your engaging Facebook post text goes here (max 300 words).",
  "{IMAGE_GENERATION_PROMPT}": "A detailed prompt for image generation AI related to the event."
}}
"""

# --- Facebook Graph API Configuration ---
GRAPH_API_VERSION = "v23.0"
PUBLISH_WHEN_POSTED = 'true' # Boolean string for Facebook API (true for immediate publish, false for draft)
IMAGE_FILE_NAME = 'image.png' # Default filename for the image when posting to Facebook
IMAGE_FILE_TYPE = 'image/png' # MIME type of the image file

# --- AI Model Configuration for Image Generation (Bedrock) ---
IMAGE_GENERATION_MODEL = 'stability.sd3-5-large-v1:0'
IMAGE_ASPECT_RATIO = "16:9" # Desired aspect ratio for generated images (e.g., "16:9", "1:1", "4:3")
IMAGE_GENERATION_MODE = "text-to-image" # Mode of image generation (e.g., "text-to-image")
IMAGE_OUTPUT_FORMAT = "png" # Output format for the generated image (e.g., "png", "jpeg")