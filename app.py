import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyBmf78vwaOdRV1ifxWHGE66xG4AuGYhWIM"))  

# Function to get response from Gemini
def get_gemini_response(input_prompt, image_parts, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_parts[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")

# Input prompt templates
prompts = {
    "Weight Loss Journey": """
    You are an expert in nutrition where you need to see the food items from the image,
    calculate the total calories, and determine if the meal is appropriate for weight loss.
    Provide the details of each food item with calorie intake and indicate if the meal is appropriate for weight loss in the following format:
    1. Item 1 - no of calories
    2. Item 2 - no of calories
    Total calories: X
    \nIs the meal appropriate for weight loss: Yes, appropriate calories/No, need more calories
    """,
    "Managing Diabetes": """
    You are an expert in diabetes management where you need to see the food items from the image,
    calculate the total carbohydrates, and determine if the meal is appropriate for diabetes management.
    Provide the details of each food item with carbohydrate content and indicate if the meal is appropriate for diabetes management in the following format:
    1. Item 1 - carbs grams, glycemic index
    2. Item 2 - carbs grams, glycemic index
    Total carbohydrates: X grams
    \nIs the meal appropriate for diabetes management: Yes, appropriate calories/No, need more calories
    """,
    "Building Muscle": """
    You are an expert in muscle-building nutrition where you need to see the food items from the image,
    calculate the total protein intake, and determine if the meal is appropriate for muscle building.
    Provide the details of each food item with protein content and indicate if the meal is appropriate for muscle building in the following format:
    1. Item 1 - protein grams
    2. Item 2 - protein grams
    Total protein: X grams
    \nIs the meal appropriate for muscle building: Yes, appropriate calories/No, need more calories
    """
}

# Scenario selection
st.header("Select Your Scenario")
scenario = st.selectbox("Choose your scenario", ["Weight Loss Journey", "Managing Diabetes", "Building Muscle"])

# Input section based on scenario
st.header("Personal Information")
name = st.text_input("Name", "User")
age = st.number_input("Age", value=28, min_value=1, max_value=100)
goal_weight_loss = goal_weight_gain = None
activity_level = diet_preference = calorie_goal = nutrient_focus = None

if scenario == "Weight Loss Journey":
    goal_weight_loss = st.number_input("Goal Weight Loss (pounds)", value=15, min_value=1)
    activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
    diet_preference = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
elif scenario == "Managing Diabetes":
    diet_preference = st.selectbox("Diet Preference", ["Low-Carb", "Balanced", "Other"])
elif scenario == "Building Muscle":
    goal_weight_gain = st.number_input("Goal Weight Gain (pounds)", value=10, min_value=1)
    activity_level = st.selectbox("Activity Level", ["Moderate", "High", "Very High"])
    diet_preference = st.selectbox("Diet Preference", ["High-Protein", "Balanced", "Other"])

# Dietary and Health Goals
st.header("Dietary and Health Goals")
calorie_goal = st.number_input("Daily Calorie Goal", value=1500, min_value=500, max_value=3000)
if scenario == "Building Muscle":
    nutrient_focus = st.multiselect("Nutrient Focus", ["Protein", "Carbs", "Fats", "Vitamins", "Minerals"])

# Meal Logging Section
st.header("Log Your Meals")
uploaded_file = st.file_uploader("Upload Meal Photo", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Sync Fitness Tracker (placeholder for future integration)
st.header("Sync Fitness Tracker")
fitness_data = st.file_uploader("Upload Fitness Tracker Data", type=["csv", "json"])

# Submit button for analysis
submit = st.button("Analyze Meal")

if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        input_prompt = prompts[scenario]
        personalized_prompt = f"Hello {name}, " + input_prompt
        response = get_gemini_response(personalized_prompt, image_data, "")
        st.subheader("The Response is")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))


