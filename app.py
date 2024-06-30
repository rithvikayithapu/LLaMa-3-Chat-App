import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models.ollama import ChatOllama
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.agents import ( create_structured_chat_agent, AgentExecutor )
from langchain import hub

load_dotenv()

# Creating memory for chat history
def get_session_history(session_id):
    return StreamlitChatMessageHistory(key=session_id)

if __name__ == "__main__":
    # Instantiating Google Search tool
    google_search = GoogleSearchAPIWrapper()
    google_tool = Tool(
        name="google-search",
        description="Search Google for recent results.",
        func=google_search.run
    )
    
    # chat_model contains the LLaMa model that generates the result.
    # prompt contains instructions for how the query should be processed. 
    # agent binds the chat_model, prompt and Google Search tool together.
    # agent_executor is used to invoke the agent on any given input.
    # To maintain context between messages agent_with_chat_history is used.
    # The chat history is retained until the Streamlit session is active.
    chat_model = ChatOllama(model="llama3", temperature=0.5)

    prompt = hub.pull("hwchase17/structured-chat-agent")

    agent = create_structured_chat_agent(chat_model, [google_tool], prompt)

    agent_executor = AgentExecutor(agent=agent, tools=[google_tool], verbose=True, handle_parsing_errors=True, max_iterations=5)

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    # Streamlit UI components
    st.title("LLaMa 3 Web Search")
    st.subheader("AI enhanced web search")

    input = st.text_area("What do you want to know?")

    if st.button("Search"):
        if input:
            with st.spinner("Generating response..."):
                res = agent_with_chat_history.invoke({"input": input}, config={"configurable": {"session_id":"<foo>"}})
                if res["output"] == "Agent stopped due to iteration limit or time limit.": 
                    st.write("Search timed out, please try again")
                else:
                    st.write(res["output"])
            