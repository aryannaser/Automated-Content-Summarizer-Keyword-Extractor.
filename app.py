import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import SUMMARIZE_TEXT_PROMPT_TEMPLATE, EXTRACT_KEYWORDS_PROMPT_TEMPLATE
from utils import fetch_article_text_from_url

# Load environment variables
load_dotenv()

# --- LLM Configuration ---
LLM_PROVIDER = "google" # or "openai" - Change this to switch

llm = None
try:
    if LLM_PROVIDER == "google":
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            st.error("GOOGLE_API_KEY not found in .env file.")
            st.stop()
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=GOOGLE_API_KEY, temperature=0.3)
    # elif LLM_PROVIDER == "openai":
    #     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    #     if not OPENAI_API_KEY:
    #         st.error("OPENAI_API_KEY not found in .env file.")
    #         st.stop()
    #     llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.3)
    else:
        st.error(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
        st.stop()
except Exception as e:
    st.error(f"Error initializing LLM: {e}")
    st.stop()
# --- End LLM Configuration ---

def get_summary(text_content: str, length_preference: str = "a few key sentences") -> str:
    if not llm or not text_content.strip():
        return "LLM not initialized or no text provided."

    prompt = PromptTemplate.from_template(SUMMARIZE_TEXT_PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    try:
        summary = chain.invoke({
            "text_to_summarize": text_content,
            "summary_length_preference": length_preference
        })
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return "Failed to generate summary."

def get_keywords(text_content: str) -> str: # Returns comma-separated string
    if not llm or not text_content.strip():
        return "LLM not initialized or no text provided."

    prompt = PromptTemplate.from_template(EXTRACT_KEYWORDS_PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    try:
        keywords = chain.invoke({"text_to_analyze": text_content})
        return keywords
    except Exception as e:
        st.error(f"Error extracting keywords: {e}")
        return "Failed to extract keywords."

def main():
    st.set_page_config(page_title="AI Content Analyzer", page_icon="📰")
    st.header("AI Content Summarizer & Keyword Extractor 📰")

    input_type = st.radio("Select input type:", ("Text", "URL"), key="input_type_selector")

    text_to_process = ""

    if input_type == "Text":
        text_to_process = st.text_area("Paste your text here:", height=200, key="text_input_area")
    elif input_type == "URL":
        url_input = st.text_input("Enter article URL:", key="url_input_field")
        if url_input:
            with st.spinner(f"Fetching content from {url_input}..."):
                # Install newspaper3k if you get an error here
                try:
                    fetched_text = fetch_article_text_from_url(url_input)
                    if fetched_text and len(fetched_text.strip()) > 100:  # Ensure we got meaningful content
                        text_to_process = fetched_text
                        preview_text = fetched_text[:1000] + "..." if len(fetched_text) > 1000 else fetched_text
                        st.text_area("Fetched Text (Preview):", value=preview_text, height=150, disabled=True)
                    else:
                        st.error("Could not extract meaningful text from the URL. The site may be protected against scraping, require login, or have restricted content.")
                        st.info("Try with a different URL or paste the text directly in the text input area.")
                except Exception as e:
                    st.error(f"Error accessing URL: {e}")
                    st.info("Many academic and news sites block web scraping. Try with a different URL or paste the text directly.")

    if text_to_process:
        if st.button("Analyze Content", key="analyze_button"):
            with st.spinner("AI is analyzing..."):
                summary = get_summary(text_to_process)
                keywords_str = get_keywords(text_to_process)

                st.subheader("📝 Summary:")
                st.write(summary)

                st.subheader("🔑 Keywords:")
                # Display keywords nicely
                if keywords_str and "Failed" not in keywords_str:
                    keyword_list = [kw.strip() for kw in keywords_str.split(',')]
                    # Using st.markdown for better visual separation or st.chip (new in Streamlit)
                    # For now, just join them back or display as list
                    st.write(", ".join(keyword_list))
                    # Or for chips (if Streamlit version supports it well, or use custom component):
                    # for kw in keyword_list:
                    # st.chip(kw) # Needs st_keyup or similar for proper chip display if using older Streamlit
                else:
                    st.write(keywords_str) # Display error if any
        else:
            st.info("Enter text or a URL and click 'Analyze Content'.")

if __name__ == '__main__':
    main() 