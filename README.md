# Thought of the Day

A LangChain application to generate inspirational thoughts.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with `OPENAI_API_KEY`.
3. Run: `python src/main.py`
4. Run the Streamlit UI: streamlit run src/ui.py

## Project Structure

- [ ] `src/`: Application code.
- [ ] `tests/`: Unit tests.
- [ ] `.env`: API keys (not tracked).

## Application Flow
The following diagram illustrates the workflow of the "Thought of the Day" application:

```mermaid
graph TD
    A[User Input: Theme or Empty] -->|app.py or ui.py| B[ThoughtGenerator]
    B -->|Instantiates| C[ThoughtPromptTemplate]
    C -->|get_thought_prompt| D[ChatPromptTemplate]
    B -->|Loads| E[ConversationBufferMemory]
    E -->|Provides chat_history| F[Chain: Prompt + LLM + Parser]
    D -->|System + Human + History| F
    F -->|Calls OpenAI GPT-4o| G[Generate Thought]
    G -->|Returns JSON| H["Output: {{thought, theme}}"]
    H -->|Saves to Memory| E
    H -->|Prints| I[Console or Streamlit UI]
