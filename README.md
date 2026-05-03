# Echoes of a Badge (The Doorway of 1973)

**CSE 358 Introduction to Artificial Intelligence - Creative Project**
**Project:** "Knock! Design Your Door"

This project is a web-based interactive digital artwork conceptualized around Bob Dylan's 1973 song "Knockin' on Heaven's Door". It allows the user to write down an emotional or physical "farewell" and, through the synergy of two LLMs, visualizes their transition.

## Technical Architecture Overview
This project uses **Streamlit** as a fast and lightweight front-end mechanism. The pipeline integrates two distinct generative AI techniques relying on the OpenAI Python API:
1. **LLM Text Generation (`gpt-4o-mini`)**: It acts as a specialized poet prompt-engineered with the philosophical mindset of the 1973 counterculture era, generating a 4-line reflective response to the user's farewell.
2. **Diffusion Image Generation (`dall-e-2`)**: It takes the semantic core and aesthetic atmosphere of the generated poem as its input prompt, outputting a visual representation of "The Door" the user is crossing.

The dual-AI pipeline takes an abstract human emotion, processes it into lyrical text via the first model, and visualizes the text using the second, satisfying the project constraints creatively.

## Installation & Setup
1. **Clone the repository** to your local environment.
2. Create and activate a Virtual Environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and place your OpenAI API key inside:
   ```env
   OPENAI_API_KEY="your-api-key-here"
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Example Usage
- **User input:** "I am leaving my childhood behind"
- The app will generate a 4-line poem representing this transition.
- The app will immediately generate a DALL-E image visually depicting this transition via a door metaphor.
