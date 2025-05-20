# AI Content Summarizer & Keyword Extractor

## Overview

This application uses advanced language models to automatically summarize text content and extract relevant keywords. It can process both direct text input and content from web URLs, making it a versatile tool for content analysis, research, and information digestion.

![AI Content Summarizer Screenshot](https://i.imgur.com/xxxxxxx.png) <!-- Replace with an actual screenshot when available -->

## Features

- **Dual Input Methods**: Process text directly or extract content from web URLs
- **Smart Content Extraction**: Advanced web scraping capabilities with fallback mechanisms
- **AI-Powered Summarization**: Generate concise summaries that capture key information
- **Intelligent Keyword Extraction**: Identify and extract the most relevant keywords from content
- **Modern UI**: Clean, responsive interface built with Streamlit
- **Flexible LLM Support**: Compatible with Google Gemini (default) and OpenAI models

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-content-summarizer.git
   cd ai-content-summarizer
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. If you encounter issues with `lxml.html.clean`, install the required package:
   ```bash
   pip install "lxml[html_clean]" lxml_html_clean
   ```

4. Set up your API keys:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file to add your API key(s).

## Configuration

### API Keys

The application requires an API key from one of the following providers:

#### Google Gemini (Default)
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Add it to your `.env` file as `GOOGLE_API_KEY="your_key_here"`

#### OpenAI (Alternative)
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an API key
3. Uncomment the OpenAI section in `app.py` and `requirements.txt`
4. Add your key to your `.env` file as `OPENAI_API_KEY="your_key_here"`

### Choosing Your LLM Provider

In `app.py`, you can set your preferred LLM provider by changing:
```python
LLM_PROVIDER = "google"  # Change to "openai" if preferred
```

## Usage

### Starting the Application

Run the application with Streamlit:
```bash
streamlit run app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501) in your web browser.

### Analyzing Text Content

1. Select "Text" from the input type options
2. Paste your content into the text area
3. Click "Analyze Content"
4. View the generated summary and extracted keywords

### Analyzing Web Content

1. Select "URL" from the input type options
2. Enter the URL of the article or page you want to analyze
3. Click "Analyze Content"
4. View the generated summary and extracted keywords

## Technical Details

### Component Overview

- **app.py**: Main Streamlit application with UI and LLM integration
- **utils.py**: Web scraping functionality using newspaper3k and BeautifulSoup
- **prompts.py**: LLM prompt templates for summarization and keyword extraction

### NLP Processing Pipeline

1. **Content Acquisition**: Via direct input or web scraping
2. **Preprocessing**: Text cleaning and preparation
3. **LLM Processing**: Sending content to language model with specific prompts
4. **Result Formatting**: Presenting summary and keywords in a readable format

### Web Scraping Capabilities

The application uses a two-tier approach for extracting content from URLs:

1. **Primary Method**: Uses `newspaper3k` library for article extraction
2. **Fallback Method**: Uses `BeautifulSoup` for manual HTML parsing
3. **Anti-Bot Avoidance**: Implements random user agents and sensible delays

## Limitations

- Some websites with strict anti-scraping measures may block content extraction
- Very large text inputs may need to be split to work within LLM token limits
- Academic journals and paywalled content typically cannot be scraped directly

## Troubleshooting

### Common Issues

**Issue**: "Could not extract meaningful text from the URL"
**Solution**: The website likely has anti-scraping measures. Try using the text input method instead.

**Issue**: LLM API errors
**Solution**: Verify your API key is correctly set in the `.env` file and that you have available quota/credits.

**Issue**: Import errors with `lxml.html.clean`
**Solution**: Run `pip install "lxml[html_clean]" lxml_html_clean` to install the required packages.

## Future Improvements

- Support for PDF document analysis
- Custom summary length options
- Multiple language support
- Sentiment analysis integration
- Topic classification features
- Saving and exporting results

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [LangChain](https://python.langchain.com/docs/get_started/introduction) for LLM integration
- [Streamlit](https://streamlit.io/) for the web interface
- [newspaper3k](https://newspaper.readthedocs.io/) for article extraction
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing 