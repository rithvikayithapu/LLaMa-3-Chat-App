# LLaMa 3 Web Search

An LLM app made with Ollama, LangChain and Streamlit.

## Run the application on your system

1. Install Ollama from [Ollama](https://ollama.com/)

2. Download LLaMa 3 

```
ollama pull llama3
```

3. Clone the repository

4. Create a Virtual Environment and activate it

```
conda create --name <my-env>
```

```
conda activate <my-env>
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Create a project on [Google Cloud Console](https://console.cloud.google.com/welcome) and get an [API Key](https://console.cloud.google.com/apis/credentials). Create a new file named .env and add this API key.

```
GOOGLE_API_KEY=your-google-api-key
```

7. Create a Google Custom Search Engine key from [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create). Select "Search the entire web" under What to Search? Add this to .env file

```
GOOGLE_CSE_ID=your-google-cse-key
```

8. Run the app

```
streamlit run app.py
```