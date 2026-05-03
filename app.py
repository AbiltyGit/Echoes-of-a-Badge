import streamlit as st
import os
import json
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
        margin-bottom: 1rem;
    }
    .emotion-tag {
        text-align: center;
        color: #d4af37;
        font-size: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .audio-label {
        font-size: 0.9rem;
        color: #888;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
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
        with st.spinner("Interpreting your farewell..."):
            try:
                # Part 1: LLM text generation and sentiment extraction via JSON mode
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a poet deeply inspired by Bob Dylan's 1973 era. Respond ONLY in valid JSON format with three keys: 'poem' (a 4-line stanza interpreting the user's farewell), 'emotion' (1 or 2 words defining the core emotion, e.g., 'Melancholic', 'Resigned', 'Hopeful'), and 'ambient_whisper' (a 1-sentence poetic description of what the atmosphere behind this emotional door sounds like, e.g. 'A cold breeze rattles the rusted iron hinges.')."},
                        {"role": "user", "content": f"Transform this farewell into our specified JSON: {user_input}"}
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=200,
                    temperature=0.7
                )
                
                data = json.loads(completion.choices[0].message.content)
                poem = data.get("poem", "")
                emotion = data.get("emotion", "Nostalgic")
                ambient_whisper = data.get("ambient_whisper", "Silence falls.")
                
                st.markdown(f"<div class='emotion-tag'>Detected Resonance: {emotion}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='poem'>{poem.replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                
                # Part 2: Generative Audio (TTS for the poem)
                st.markdown("<div class='audio-label'>Voice of the Wanderer (Poem):</div>", unsafe_allow_html=True)
                poem_audio_response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=poem
                )
                poem_audio_response.stream_to_file("poem.mp3")
                st.audio("poem.mp3", format="audio/mp3")

                # Part 3: Text-To-Image using Poem and Emotion
                with st.spinner("Visualizing your new door..."):
                    img_prompt = f"Abstract, {emotion} 1970s aesthetic, vintage photography style. A symbolic door representing transition. The visual atmosphere perfectly reflects this poem: {poem}"
                    
                    response = client.images.generate(
                        model="dall-e-2",
                        prompt=img_prompt,
                        size="512x512",
                        n=1,
                    )
                    image_url = response.data[0].url
                    st.image(image_url, caption="Your Door", use_container_width=True)

                # Part 4: Generative Audio (TTS for the visual atmosphere/ambient whisper)
                st.markdown("<div class='audio-label'>Whisper of the Door (Atmosphere):</div>", unsafe_allow_html=True)
                ambient_audio_response = client.audio.speech.create(
                    model="tts-1",
                    voice="fable",
                    input=ambient_whisper
                )
                ambient_audio_response.stream_to_file("ambient.mp3")
                st.audio("ambient.mp3", format="audio/mp3")
                st.write(f"*(The door whispers: \"{ambient_whisper}\")*")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your farewell before knocking.")
