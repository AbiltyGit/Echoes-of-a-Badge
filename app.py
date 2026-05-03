import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Echoes of a Badge",
    page_icon="🚪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for dark theme
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Georgia', serif;
    }
    .main-header {
        font-size: 3rem;
        text-align: center;
        color: #d4af37;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #aaaaaa;
        font-style: italic;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .poem {
        font-size: 1.5rem;
        text-align: center;
        font-style: italic;
        background-color: rgba(20, 20, 20, 0.8);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #333;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Echoes of a Badge</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Mama, take this badge off of me... I can't use it anymore.</p>", unsafe_allow_html=True)

st.write("What are you leaving behind today? What door are you knocking on?")

with st.form(key='farewell_form'):
    user_input = st.text_input("Enter your farewell (e.g., 'I am leaving my childhood behind', 'I surrender my fears'):")
    submit_button = st.form_submit_button(label="Knock on Heaven's Door")

if submit_button:
    if user_input:
        with st.spinner("Writing the echoes of your farewell..."):
            try:
                # Part 1: LLM Metin Üretimi
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a poet deeply inspired by Bob Dylan's 1973 era, specifically the melancholy and philosophical transition of 'Knockin' on Heaven's Door'. Respond strictly with a 4-line stanza interpreting the user's farewell."},
                        {"role": "user", "content": f"Transform this farewell into a poem: {user_input}"}
                    ],
                    max_tokens=60,
                    temperature=0.7
                )
                poem = completion.choices[0].message.content.strip()
                
                st.markdown(f"<div class='poem'>{poem.replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                
                # Part 2: Image Generation
                with st.spinner("Visualizing your new door..."):
                    img_prompt = f"Abstract, melancholic 1970s aesthetic, vintage photography style. A symbolic door representing transition. The atmosphere reflects this poem: {poem}"
                    
                    response = client.images.generate(
                        model="dall-e-2",
                        prompt=img_prompt,
                        size="512x512",
                        n=1,
                    )
                    image_url = response.data[0].url
                    
                    st.image(image_url, caption="Your Door", use_container_width=True)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your farewell before knocking.")
