import streamlit as st
from utils.thought_generator import ThoughtGenerator
import json


# Page configuration
st.set_page_config(page_title="Thought of the Day", page_icon="🌟", layout="centered")

# Initialize ThoughtGenerator
generator = ThoughtGenerator()

# UI Layout
st.title("🌟 Thought of the Day")
st.write("Enter a theme (e.g., motivation, peace) or leave blank for a random thought.")

# Input form
with st.form(key="thought_form"):
    theme = st.text_input(
        "Theme (optional):", placeholder="e.g., motivation, peace, happiness"
    )
    submit_button = st.form_submit_button(label="Generate Thought")

# Handle form submission
if submit_button:
    with st.spinner("Generating your thought..."):
        result = generator.get_thought(theme)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            # Display formatted JSON output
            st.subheader("Your Thought of the Day")
            st.json(result)  # Displays JSON nicely
            # Additional styled display
            st.markdown(
                f"""
                **Thought**: {result['thought']}  
                **Theme**: {result['theme']}
                """,
                unsafe_allow_html=True,
            )
