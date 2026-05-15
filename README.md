<<<<<<< HEAD
# SecureDoc - PDF Q&A Application with OpenAI

A modern web application built with Streamlit that allows you to upload PDFs and ask questions about them using OpenAI's GPT models.

## Features

✨ **Key Features:**
- 📤 Upload and process PDF documents
- 🤖 Ask questions about PDF content using OpenAI GPT models
- 🔍 Semantic search with vector embeddings
- 📚 Source document tracking and display
- ⚙️ Configurable model parameters (temperature, chunk size, etc.)
- 🔐 Secure and private document processing
- 🎨 Beautiful, responsive web interface

## Requirements

- **Python 3.10** (or higher)
- OpenAI API Key (get one at https://platform.openai.com/api-keys)
- Windows (or use run_linux.sh for Linux/Mac)

## Quick Start

### 1. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (you'll need it in step 4)

### 2. Set Your API Key (Choose One Method)

#### Method A: Environment Variable (Temporary)
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

#### Method B: .env File (Recommended)
1. Open `.env.example` in your editor
2. Replace `sk-your-api-key-here` with your actual API key
3. Rename the file from `.env.example` to `.env`

#### Method C: Windows Environment Variable (Permanent)
1. Press `Win + X`, select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" under "User variables"
5. Variable name: `OPENAI_API_KEY`
6. Variable value: `sk-your-api-key-here`
7. Click OK and restart your terminal

### 3. Run the Application

Simply double-click **`run.bat`** in the SecureDoc folder

The application will:
- Create a Python 3.10 virtual environment
- Install all dependencies
- Start the web interface at `http://localhost:8501`

### 4. Use SecureDoc

1. Upload a PDF file using the file uploader
2. Configure settings in the left sidebar (model, temperature, etc.)
3. Ask questions about the PDF content
4. View answers with source document references

## Configuration Options

### Model Selection
- **gpt-4-turbo**: Most powerful, best for complex questions (higher cost)
- **gpt-4**: Balanced performance and quality
- **gpt-3.5-turbo**: Fastest and most economical

### Temperature
- **0.0**: Deterministic, focused responses
- **0.7**: Default, balanced creativity and consistency
- **2.0**: Maximum randomness and creativity

### Chunk Settings
- **Chunk Size**: How large each text segment is (200-2000 characters)
- **Chunk Overlap**: How much text overlaps between chunks (0-500 characters)

## Troubleshooting

### Error: "Python 3.10 not found"
- Download and install Python 3.10 from https://www.python.org/downloads/
- When installing, check "Add Python 3.10 to PATH"

### Error: "OPENAI_API_KEY not found"
- Follow the "Set Your API Key" instructions above
- Restart your terminal after setting the environment variable
- Verify your API key is correct at https://platform.openai.com/api-keys

### Error: "ModuleNotFoundError"
- Delete the `venv310` folder
- Run `run.bat` again to recreate the virtual environment

### Slow Performance
- Your OpenAI API might be rate-limited
- Try using gpt-3.5-turbo instead of gpt-4
- Reduce the chunk size in the sidebar

## Project Structure

```
SecureDoc/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run.bat               # Windows launcher script
├── .env.example          # Example environment configuration
├── .env                  # Your API keys (create from .env.example)
└── venv310/              # Python virtual environment (created automatically)
```

## How It Works

1. **PDF Loading**: Uses PyPDFLoader to extract text from uploaded PDFs
2. **Text Chunking**: Splits large documents into manageable chunks
3. **Embeddings**: Creates vector embeddings using OpenAI's embedding model
4. **Vector Database**: Stores embeddings in Chroma for fast retrieval
5. **QA System**: Uses LangChain's RetrievalQA to answer questions
6. **Response Generation**: Streams answers back through the web interface

## Security

- Your PDFs are processed locally and not stored
- API key is kept in your local environment, never logged
- Temporary files are cleaned up automatically
- Supports both local and cloud deployments

## Cost Considerations

Using this application will incur costs based on OpenAI API usage:
- **Embedding API**: ~$0.02 per 1M tokens
- **GPT-3.5-turbo**: ~$0.001-0.002 per 1K tokens
- **GPT-4-turbo**: ~$0.01 per 1K tokens

Monitor your usage at https://platform.openai.com/usage

## Advanced Usage

### Manual Virtual Environment Setup
```powershell
# Create venv
py -3.10 -m venv venv310

# Activate venv
.\venv310\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Run on Linux/Mac
```bash
python3.10 -m venv venv310
source venv310/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Support

For issues with:
- **Streamlit**: https://discuss.streamlit.io/
- **LangChain**: https://github.com/langchain-ai/langchain
- **OpenAI**: https://help.openai.com/

## License

This project is provided as-is for educational and personal use.

## Updates

To update dependencies:
```powershell
.\venv310\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

---

**Created**: May 2026
**Python Version**: 3.10+
**Status**: ✅ Ready to Use
=======
# private-Q-A-using-RAG
this is my 6th sem project
>>>>>>> efa297e460a8005f1559196bae9360b98e9bed35
