from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY="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"
# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=200,
    openai_api_key=OPENAI_API_KEY
)

# Initialize memory
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
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
    Return the output as a JSON object with 'thought' and 'theme' fields.
    """)
])

# Set up the output parser
parser = JsonOutputParser()

# Create the chain
chain = prompt | llm | parser

def get_thought_of_the_day(theme=""):
    try:
        # Load conversation history
        memory_context = memory.load_memory_variables({})
        
        # Invoke the chain
        result = chain.invoke({
            "theme": theme or "random",
            "chat_history": memory_context["chat_history"]
        })
        
        # Save the interaction to memory
        memory.save_context(
            inputs={"human": f"Theme: {theme or 'random'}"},
            outputs={"assistant": json.dumps(result)}
        )
        
        return result
    
    except Exception as e:
        return {"error": f"Failed to generate thought: {str(e)}"}

# Example usage
def main():
    print("Welcome to Thought of the Day!")
    
    # Interaction 1: User specifies a theme
    print("\nGenerating thought for theme: 'motivation'")
    result1 = get_thought_of_the_day("motivation")
    print(json.dumps(result1, indent=2))
    
    # Interaction 2: No theme (random)
    print("\nGenerating thought with random theme")
    result2 = get_thought_of_the_day()
    print(json.dumps(result2, indent=2))
    
    # Interaction 3: Another theme, with memory
    print("\nGenerating thought for theme: 'peace'")
    result3 = get_thought_of_the_day("peace")
    print(json.dumps(result3, indent=2))

if __name__ == "__main__":
    main()