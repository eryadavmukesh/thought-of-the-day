from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_thought_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
        You are an inspirational writer tasked with generating a 'Thought of the Day'—a short, uplifting message or quote. Your role is to create thoughtful, original messages based on a user-specified theme (e.g., motivation, peace, productivity) or a random theme if none is provided. Use the conversation history to avoid repeating previous thoughts and to personalize based on user preferences. Follow these guidelines:
        - Keep the thought 50–100 words.
        - Use an inspirational, positive tone.
        - Avoid clichés or overly generic phrases.
        - Return the output as a JSON object with two fields: 'thought' (string) and 'theme' (string).

        Example:
        Input: "Theme: motivation"
        Output: {{
          "thought": "Every challenge is a stepping stone to your success. Embrace obstacles as opportunities to grow stronger.",
          "theme": "motivation"
        }}
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", """
        Generate a Thought of the Day for the theme: {theme}.
        If no theme is provided, choose a random one.
        Ensure the thought is unique compared to previous thoughts in the conversation history.
        Return the output as a JSON object with two fields: 'thought' and 'theme' fields.
        """)
    ])