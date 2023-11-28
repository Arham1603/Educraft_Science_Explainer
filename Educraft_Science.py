from streamlit_option_menu import option_menu
#from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import requests 
import time
import os

#load_dotenv()

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

client = OpenAI(
  api_key=OPENAI_API_KEY
)

# Preference options
subjects = ['Any', 'Biology', 'Chemistry', 'Physics']
preferred_learning_styles = ['Any', 'Detailed explanations', 'Examples', 'Real-world applications']
specific_challenges = ['Any', 'Conceptual understanding', 'Problem-solving']
prior_knowledge = ['Any', 'Limited', 'Moderate', 'Advanced']
preferred_interaction = ['Any', 'Socratic questioning', 'Interactive discussions']
preferred_difficulty = ['Any', 'Easy', 'Moderate', 'Challenging']
preferred_support = ['Any', 'Patient and understanding', 'Providing constructive criticism', 'Offering positive reinforcement']
preferred_language = ['Any', 'English', 'Tamil', 'Mandarin']

def teacher_ai(subjects, preferred_learning_styles, specific_challenges, current_topic, prior_knowledge,
               preferred_interaction, preferred_difficulty, preferred_support, preferred_language):
    system_prompt = """
    You are a highly experienced secondary school science teacher with 20 years of expertise, specializing in physics,
    biology, and chemistry. You are providing guidance and explanations to students on various scientific concepts. 
    Tailor your responses to address the specific needs and difficulties that secondary school students commonly 
    encounter in these subjects. Offer detailed explanations, examples, and practical applications to enhance 
    understanding. Incorporate common misconceptions and highlight key points to reinforce the learning process. Keep 
    in mind the academic level of secondary school students and maintain a supportive and encouraging tone throughout 
    the interactions.
    """
    input_prompt = f"""
    I am a senior high school student seeking assistance in {subjects}. I prefer learning through {preferred_learning_styles} 
    and currently facing challenges in {specific_challenges}. The specific topic or problem I need help with is "{current_topic}". 
    In terms of prior knowledge, I would rate myself as having a {prior_knowledge} level. I also enjoy {preferred_interaction} 
    as a learning method, and I find content of {preferred_difficulty} level suits me best. I appreciate guidance that is 
    {preferred_support}. I prefer explanations in {preferred_language}. Please include emoji as much as possible. Please 
    provide assistance considering these learning preferences.
    """

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{
                        "role":"system",
                        "content": system_prompt
                    },
                    {
                        "role":"user",
                        "content": input_prompt
                    }
        ],
        max_tokens = 3000,
        temperature = 0.8,
    )

    # Extract and return the generated lesson plan
    return response.choices[0].message.content

def formula_ai(msg):
    system_prompt = """
    As an accomplished secondary school science teacher with over 20 years of expertise, specializing in physics, 
    biology, and chemistry, your role is crucial in imparting knowledge of intricate scientific formulas and concepts. 
    Tailor your responses to address the unique needs and challenges that secondary school students often face in 
    comprehending and applying these formulas. Provide in-depth explanations, practical examples, and real-world 
    applications to enrich their understanding. Emphasize the importance of mastering key formulas, dispel common 
    misconceptions, and foster a strong grasp of these scientific principles. Your goal is to elevate students' 
    proficiency in handling and manipulating formulas, considering their academic level, and maintaining a supportive 
    and encouraging tone throughout your interactions. Please include emoji as much as possible.
    """

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{
                        "role":"system",
                        "content": system_prompt
                    },
                    {
                        "role":"user",
                        "content": f'{msg}'
                    }
        ],
        max_tokens = 3000,
        temperature = 0.8,
    )

    # Extract and return the generated lesson plan
    return response.choices[0].message.content

def experiment_ai(msg):
    system_prompt = """
    As an experienced secondary school science teacher with over 20 years of expertise in physics, biology, and chemistry, 
    your role is pivotal in guiding students through engaging and insightful laboratory experiments. Tailor your responses 
    to provide clear and detailed lab manuals for the specific needs and challenges that secondary school students commonly 
    encounter in designing, conducting, and understanding experiments. Your task is to create comprehensive instructions, 
    practical examples, and real-world applications that serve as effective lab manuals. Emphasize the significance of each 
    step in the experimental process, clarify common misconceptions, and inspire a deeper appreciation for the scientific 
    method. Your goal is to foster a curiosity for experimentation. Keep in mind the academic level of secondary school 
    students and maintain a supportive and encouraging tone throughout the interactions.. Feel free to include emojis 
    to make the learning experience even more enjoyable! 🧪🔬👩‍🔬👨‍🔬
    """

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{
                        "role":"system",
                        "content": system_prompt
                    },
                    {
                        "role":"user",
                        "content": f'{msg}'
                    }
        ],
        max_tokens = 3000,
        temperature = 0.8,
    )

    # Extract and return the generated lesson plan
    return response.choices[0].message.content

def summarizer_ai(msg):
    system_prompt = """
    You have a skill for condensing information, extracting crucial keywords, and crafting engaging YouTube video titles.
    Your expertise shines when summarizing content, ensuring it captures the essence effectively, especially prioritizing 
    science aspects, especially in physics, biology, and chemistry. After considering these factors, select the most impactful title. 
    Make sure the title chosen is related to the science.
    """
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{
                        "role":"system",
                        "content": system_prompt
                    },
                    {
                        "role":"user",
                        "content": f'{msg}'
                    }
        ],
        max_tokens = 3000,
        temperature = 1.0,
    )

    return response.choices[0].message.content

def find_ai(msg):
    system_prompt = """
    Your expertise lies in summarizing content and identifying crucial science formulas, especially in chemistry, physics, and 
    biology for secondary school.  Your goal is to find the most important science formula related to the given 
    content for a Google image search. Consider the key aspects and prioritize the formula that encapsulates the core of 
    the information. Then write one formula only. Don't write anything else.
    """
    instruction = """
    👩‍🏫 Sure! I'd be happy to help you with understanding the concept of "Speed" in physics. Speed is a fundamental concept that 
    describes how fast an object is moving. It is defined as the distance traveled by an object divided by the time taken to travel 
    that distance. The formula for speed is:

    Speed = Distance ÷ Time

    Let's break this formula down and understand each component. Distance refers to the total path covered by an object, usually 
    measured in meters (m). Time is the duration it takes for an object to travel that distance, typically measured in seconds (s). 
    When we divide the distance by the time, we get the speed of the object.

    To illustrate this concept, let's consider an example. Imagine a car traveling a distance of 100 meters in 10 seconds. By using the 
    formula, we can calculate the speed as follows:

    Speed = Distance ÷ Time Speed = 100m ÷ 10s Speed = 10 m/s

    In this case, the speed of the car is 10 meters per second.

    Now, let's discuss some real-world applications of the speed formula. Speed is used in various contexts, such as calculating the 
    velocity of a moving vehicle, determining the rate at which an object is moving, or analyzing the speed of sound or light. 
    Understanding speed is essential in fields like transportation, sports, and even astronomy.

    One common misconception students have is confusing speed with velocity. While speed refers to the rate at which an object moves, 
    velocity includes the speed and the direction in which the object is moving. So, remember that speed is just how fast or slow 
    something is moving, while velocity adds direction to that speed.

    To enhance your understanding of speed, I suggest practicing more problems and applying the formula to different scenarios. 
    You can also try to relate speed to everyday life situations to make it more relatable. If you have any specific questions or 
    examples you'd like me to help you with, feel free to ask! 😊
    """
    sample_answer = "Speed = Distance ÷ Time"
  
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{
                        "role":"system",
                        "content": system_prompt
                    },
                    {
                        "role":"user",
                        "content": instruction
                    },
                    {
                        "role":"assistant",
                        "content": sample_answer
                    },
                    {
                        "role":"user",
                        "content": f'{msg}'
                    }
        ],
        max_tokens = 3000,
        temperature = 1.0,
    )

    return response.choices[0].message.content

# Function to perform an image search using SerpAPI
@st.cache_data
def serpapi_image_search(query, num_results=5):
    # Set your SerpAPI key here
    SERPAPI_KEY = st.secrets["SERPAPI_KEY"]

    # Define SerpAPI parameters
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_images",
        "q": query,
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "device": "desktop",
    }

    # Make the SerpAPI request
    response = requests.get("https://serpapi.com/search.json", params=params).json()

    # Debugging: Display the entire SerpAPI response
    # st.write("SerpAPI Response:", response)

    # Check if image results are present in the response
    if "images_results" in response:
        # Extract image results from the response
        all_image_results = [result["original"] for result in response.get("images_results", [])]

        # Limit the results to the specified number
        image_results = all_image_results[:num_results]

        # Debugging: Display the image results
        # st.write("Image Results:", image_results)

        return image_results
    else:
        st.warning("No relevant images found.")
        return []
  
# Function to perform a video search using YoutubeAPI
@st.cache_data
def youtube_video_search(query, num_results=5):
    # Set your YouTube Data API key here
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

    # Define YouTube Data API parameters for video search
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": num_results,
        "key": YOUTUBE_API_KEY,
    }

    # Make the YouTube Data API request for video search
    response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params).json()

    # Debugging: Display the entire YouTube Data API response
    # st.write("YouTube API Response:", response)

    # Check if video results are present in the response
    if "items" in response and len(response["items"]) > 0:
        # Extract video details including title from the response
        video_results = [
            {"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"} 
            for item in response["items"]
        ]

        # Debugging: Display the video results
        # st.write("Video Results:", video_results)

        return video_results
    else:
        st.warning("No relevant videos found.")
        return []

def homepage():
    header = st.container()
    description = st.container()
    
    #background
    bg_pic = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-vector/education-presentation-template-background-science-subject-seamless-border-back-school_91515-554.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    }
    </style>

    <style>
    [data-testid="stHeader"] {
    background-image: url("https://img.freepik.com/premium-vector/education-presentation-template-background-science-subject-seamless-border-back-school_91515-554.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    }
    </style>
    """
    st.markdown(bg_pic, unsafe_allow_html=True)
    
    h1_style = """
    <style>
        .app-title {
            font-size: 60px;
            font-family: 'Times New Roman', sans-serif;
            text-align: center;
            color: #7A4717;
            margin-top: 150px;
            margin-bottom: 20px;
            white-space: nowrap;
        }
    </style>
    """
    h2_style = """
    <style>
        .subh-title {
            font-size: 35px;
            font-family: 'Times New Roman', sans-serif;
            text-align: justify;
            color: #7A4717;
        }
    </style>
    """
    #header
    with header:
       st.markdown(h1_style, unsafe_allow_html=True)
       st.markdown("""<h1 class="app-title"><strong>EduCraft: Science Explainer</strong></h1>""", unsafe_allow_html=True)
    
    #subheader
    with description:
       st.markdown(h2_style, unsafe_allow_html=True)
       st.markdown("""<h2 class="subh-title">Welcome to EduCraft, a science explainer tool designed to help secondary 
                   school students understand various science topics briefly. This app empowers students to customize 
                   their learning experience by providing concise explanations, relevant examples, and interactive 
                   content.</h2>""", unsafe_allow_html=True)

def theory_page():
   
   s1_style = """
    <style>
        .title {
            font-size: 50px;
            font-family: 'Roboto', sans-serif;
            text-align: center;
            color: #2B3A67;
            margin-bottom: 20px;
        }
    </style>
    """
   st.markdown(s1_style, unsafe_allow_html=True)
   st.markdown("""<h1 class="title"><strong>Let Educraft answer your query! </strong></h1>""", unsafe_allow_html=True)

   # Sidebar inputs
   selected_subject = st.selectbox("Select the science subject:", subjects)
   selected_learning_style = st.selectbox("Select the learning style:", preferred_learning_styles)
   selected_challenges = st.selectbox("Select the challenge you face:", specific_challenges)
   topic = st.text_area("Input your topic or question:")
   selected_knowledge = st.selectbox("Select your prior knowledge:", prior_knowledge)
   selected_interaction = st.selectbox("Select your preferred interaction:", preferred_interaction)
   selected_difficulty = st.selectbox("Select your preferred difficulty:", preferred_difficulty)
   selected_support = st.selectbox("Select your preferred support method:", preferred_support)
   selected_language = st.selectbox("Select your preferred language:", preferred_language)
   # User input for the number of videos
   num_videos = st.slider("Select the number of youtube videos you want to refer:", min_value=1, max_value=5, value=3)

   # Generate science lesson plan
   if st.button("Generate"):
        lesson_plan = teacher_ai(selected_subject, selected_learning_style, selected_challenges, topic, selected_knowledge,
                                 selected_interaction, selected_difficulty, selected_support, selected_language)

        # Display the generated lesson plan
        st.header("Generated Science Material:")
        st.write(lesson_plan)

        yt_title_search = summarizer_ai(lesson_plan)
        # Generate and display relevant images using YoutubeAPI
        video_results = youtube_video_search(yt_title_search, num_results=num_videos)

        # Display video results
        if video_results:
            st.header("Relevant YouTube videos search for extra reference:")
            for index, video_info in enumerate(video_results, start=1):
                st.write(f"**Video {index}:**")
                st.write(f"**Title:** {video_info['title']}")
                st.write(f"**Watch:** [{video_info['title']}]({video_info['url']})")
                st.video(video_info['url'])
        else:
            st.warning("No relevant videos found.")

def formula_page():
   
   s1_style = """
    <style>
        .title {
            font-size: 50px;
            font-family: 'Roboto', sans-serif;
            text-align: center;
            color: #2B3A67;
            margin-bottom: 20px;
        }
    </style>
    """
   st.markdown(s1_style, unsafe_allow_html=True)
   st.markdown("""<h1 class="title"><strong>Let Educraft explain the formula! </strong></h1>""", unsafe_allow_html=True)

   # Sidebar inputs
   selected_subject = st.selectbox("Select the science subject:", subjects)
   selected_learning_style = st.selectbox("Select the learning style:", preferred_learning_styles)
   selected_challenges = st.selectbox("Select the challenge you face:", specific_challenges)
   formula = st.text_area("Input your formula or problem:")
   selected_knowledge = st.selectbox("Select your prior knowledge:", prior_knowledge)
   # User input for the number of images
   num_images = st.slider("Select the number of images related to topic to display:", min_value=1, max_value=5, value=3)

   input_prompt = f"""
    I am a senior high school student seeking assistance in {selected_subject}. I prefer learning through {selected_learning_style} 
    and currently facing challenges in {selected_challenges}. The specific scientific formula or problem I need help with is 
    "{formula}". In terms of prior knowledge, I would rate myself as having a {selected_knowledge} level. I believe a 
    clear understanding of this formula is crucial for my studies, and I'm looking for detailed explanations and 
    applications to enhance my comprehension.
   """
    # Generate science lesson plan
   if st.button("Explain"):
        formula_explain = formula_ai(input_prompt)

        # Display the generated lesson plan
        st.header("Generated Formula Explanation:")
        st.write(formula_explain)

        image_search = find_ai(formula_explain)
        # Generate and display relevant images using SerpAPI
        image_results = serpapi_image_search(image_search, num_results=num_images)

        # Display image results
        if image_results:
            st.header("Relevant images for extra reference:")
            for image_url in image_results:
                st.image(image_url, caption="SerpAPI Result", use_column_width=True)
        else:
            st.warning("No relevant images found.")

def experiment_page():
   s1_style = """
    <style>
        .title {
            font-size: 50px;
            font-family: 'Roboto', sans-serif;
            text-align: center;
            color: #2B3A67;
            margin-bottom: 20px;
        }
    </style>
    """
   st.markdown(s1_style, unsafe_allow_html=True)
   st.markdown("""<h1 class="title"><strong>Let Educraft explain the experiment! </strong></h1>""", unsafe_allow_html=True)

   # Inputs
   selected_subject = st.selectbox("Select the science subject:", subjects)
   experiment = st.text_area("Input the name of the science experiment :")
   selected_knowledge = st.selectbox("Select your prior knowledge:", prior_knowledge)

   input_prompt = f"""
    I am a senior high school student seeking assistance in {selected_subject}. The specific experiment or problem I need help with 
    is "{experiment}". In terms of prior knowledge, I would rate myself as having a {selected_knowledge} level. I believe a clear 
    understanding of this experiment is crucial for my studies, and I'm looking for detailed explanations and applications to 
    enhance my comprehension.
    """
    # Generate Experiment explanation
   if st.button("Explain"):
        experiment_explain = experiment_ai(input_prompt)

        # Display the generated lesson plan
        st.header("Generated Experiment Explanation:")
        st.write(experiment_explain)

def main():
    st.set_page_config(
       page_title="Educraft",
       page_icon=":dragon_face:",
    )
    
    #sidebar
    sb_style = """
    <style>
        .sidebar-title {
            font-size: 24px;
            font-family: 'Baskerville', sans-serif;
            text-align: center;
            color: #2B3A67;
        }
    </style>
    """
    st.sidebar.markdown(sb_style, unsafe_allow_html=True)
    st.sidebar.markdown('<span class="sidebar-title"><strong>Explore EduCraft :computer: </strong></span>', unsafe_allow_html=True)

    page_functions = {
       "Home": homepage,
       "Theory/Concept": theory_page,
       "Formula": formula_page,
       "Experiment": experiment_page
    }

    with st.sidebar:
        selected_page = option_menu(menu_title="Choose task", options=list(page_functions.keys()), icons=['house', 'receipt', 'receipt', 'receipt'], default_index=0)

    if selected_page in page_functions:
       page_functions[selected_page]()
# %%
if __name__ == "__main__":
    main()
