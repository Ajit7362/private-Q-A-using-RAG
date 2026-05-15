import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
try:
    from langchain.chains import RetrievalQA
except (ImportError, ModuleNotFoundError):
    from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from dotenv import load_dotenv
import tempfile

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SecureDoc - PDF Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 SecureDoc - PDF Q&A with OpenAI")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write("**OpenAI Settings**")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("⚠️ No OpenAI API Key detected")
        st.info("Set your API key by:")
        st.code('$env:OPENAI_API_KEY="sk-..."', language="powershell")
    else:
        st.success("✅ OpenAI API Key configured")
    
    model = st.selectbox(
        "Select Model",
        ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        help="Choose the OpenAI model to use"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: lower = more focused, higher = more creative"
    )
    
    chunk_size = st.number_input(
        "Chunk Size",
        min_value=200,
        max_value=2000,
        value=1000,
        step=100
    )
    
    chunk_overlap = st.number_input(
        "Chunk Overlap",
        min_value=0,
        max_value=500,
        value=100,
        step=50
    )

# Main content
if not api_key:
    st.error("❌ OpenAI API Key not found!")
    st.info(
        """
        To use SecureDoc, you need to set your OpenAI API Key.
        
        **For PowerShell:**
        ```powershell
        $env:OPENAI_API_KEY = "your-api-key-here"
        ```
        
        **For Command Prompt:**
        ```cmd
        set OPENAI_API_KEY=your-api-key-here
        ```
        
        Get your API key from: https://platform.openai.com/api-keys
        """
    )
else:
    try:
        # Create temp directory for PDFs
        temp_dir = tempfile.gettempdir()
        pdf_temp_dir = os.path.join(temp_dir, "securedoc_pdfs")
        os.makedirs(pdf_temp_dir, exist_ok=True)
        
        # File uploader
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
        
        if uploaded_file is not None:
            file_path = os.path.join(pdf_temp_dir, uploaded_file.name)
            
            with st.spinner("🔄 Processing PDF..."):
                # Save temporarily
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    # Load PDF
                    loader = PyPDFLoader(file_path)
                    documents = loader.load()
                    
                    if not documents:
                        st.error("❌ Could not extract any text from the PDF")
                    else:
                        # Remove empty pages before splitting
                        documents = [doc for doc in documents if getattr(doc, 'page_content', '').strip()]
                        
                        if not documents:
                            st.error(
                                "❌ PDF pages were found, but no selectable text could be extracted. "
                                "This is common with scanned/image PDFs. Please use a text-based PDF or perform OCR first."
                            )
                        else:
                            st.info(f"📖 Loaded {len(documents)} pages with text from PDF")
                            
                            # Text Chunking
                            splitter = RecursiveCharacterTextSplitter(
                                chunk_size=chunk_size,
                                chunk_overlap=chunk_overlap
                            )
                            texts = splitter.split_documents(documents)
                            texts = [doc for doc in texts if getattr(doc, 'page_content', '').strip()]
                            st.info(f"✂️ Split into {len(texts)} chunks")
                            
                            if not texts:
                                st.error(
                                    "❌ The PDF text could not be split into chunks. "
                                    "Try reducing the chunk overlap or using a different PDF."
                                )
                            else:
                                # Create Embeddings
                                embeddings = OpenAIEmbeddings(
                                    model="text-embedding-3-small",
                                    api_key=api_key
                                )
                                
                                # Store in Vector DB
                                db = Chroma.from_documents(texts, embeddings)
                                st.info("🗄️ Created vector database")
                                
                                # Create QA System
                                llm = ChatOpenAI(
                                    model=model,
                                    temperature=temperature,
                                    api_key=api_key,
                                    max_tokens=1024
                                )
                                
                                qa = RetrievalQA.from_chain_type(
                                    llm=llm,
                                    chain_type="stuff",
                                    retriever=db.as_retriever(search_kwargs={"k": 3}),
                                    return_source_documents=True
                                )
                                
                                st.success("✅ PDF processed successfully! Ask your questions below.")
                                
                                # Query interface
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    query = st.text_input(
                                        "🔍 Ask a question about the PDF",
                                        placeholder="What is this document about?"
                                    )

                                if query:
                                    with st.spinner("🤖 Generating answer..."):
                                        try:
                                            result = qa({"query": query})

                                            # Display answer
                                            st.markdown("### 📝 Answer")
                                            st.write(result["result"])

                                            # Display source documents
                                            with st.expander("📚 Sources"):
                                                for i, doc in enumerate(result.get("source_documents", []), 1):
                                                    st.markdown(f"**Source {i}:**")
                                                    st.text(doc.page_content[:500] + "...")
                                                    st.caption(f"Page: {doc.metadata.get('page', 'N/A')}")

                                        except Exception as e:
                                            st.error(f"❌ Error generating answer: {str(e)}")
                
                finally:
                    # Clean up temp file
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("📌 Upload a PDF to get started")
            with col2:
                st.info("🚀 Powered by OpenAI GPT")
            with col3:
                st.info("🔐 Your data is secure")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please check your API key and try again.")