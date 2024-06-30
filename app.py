import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models.ollama import ChatOllama
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import ( create_structured_chat_agent, AgentExecutor )
from langchain import hub

load_dotenv()

if __name__ == "__main__":
    google_search = GoogleSearchAPIWrapper()
    google_tool = Tool(
        name="google-search",
        description="Search Google for recent results.",
        func=google_search.run
    )

    chat_model = ChatOllama(model="llama3", temperature=0.1)

    prompt = hub.pull("hwchase17/structured-chat-agent")

    agent = create_structured_chat_agent(chat_model, [google_tool], prompt)

    agent_executor = AgentExecutor(agent=agent, tools=[google_tool], verbose=False, handle_parsing_errors=True, max_iterations=3)

    st.title("LLaMa 3 Web Search")
    st.subheader("AI enhanced web search")

    input = st.text_area("What would you like to search for?")

    if st.button("Search"):
        if input:
            with st.spinner("Generating response..."):
                res = agent_executor.invoke({"input": input})
                st.write(res["output"])
            