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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SecureDoc - Syllabus Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 SecureDoc - 5th Semester Syllabus Q&A")
st.markdown("**Powered by OpenAI GPT + LangChain**")

# Get API key
api_key = os.environ.get("OPENAI_API_KEY")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    if api_key:
        st.success("✅ OpenAI API Key configured")
    else:
        st.error("❌ No API Key found")
    
    model = st.selectbox(
        "Model",
        ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=2,
        help="Choose the OpenAI model"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )
    
    chunk_size = st.number_input("Chunk Size", value=1000, min_value=200)
    chunk_overlap = st.number_input("Chunk Overlap", value=100, min_value=0)

# Error check for API key
if not api_key:
    st.error("❌ OpenAI API Key not configured!")
    st.info("Set OPENAI_API_KEY in your .env file")
    st.stop()

# Session state for caching
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
    st.session_state.qa_chain = None

# File uploader
st.divider()
uploaded_file = st.file_uploader("📁 Upload a PDF", type="pdf")

if uploaded_file is not None:
    try:
        # Create temp directory
        temp_dir = tempfile.gettempdir()
        pdf_temp_dir = os.path.join(temp_dir, "securedoc_pdfs")
        os.makedirs(pdf_temp_dir, exist_ok=True)
        
        pdf_path = os.path.join(pdf_temp_dir, uploaded_file.name)
        
        with st.spinner("🔄 Loading PDF..."):
            # Save temporarily
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            if not documents:
                st.error("❌ Could not extract text from PDF")
            else:
                st.success(f"✅ Loaded {len(documents)} pages")
                
                with st.spinner("✂️ Processing text..."):
                    # Text chunking
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                    texts = splitter.split_documents(documents)
                    st.info(f"Split into {len(texts)} chunks")
                    
                    # Create embeddings
                    embeddings = OpenAIEmbeddings(
                        model="text-embedding-3-small",
                        api_key=api_key
                    )
                    
                    # Vector database
                    db = Chroma.from_documents(texts, embeddings)
                    st.info("✅ Vector database created")
                    
                    # QA Chain
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
                    
                    st.session_state.vector_db = db
                    st.session_state.qa_chain = qa
                
                st.success("🎉 Ready! Ask your questions below.")
                st.divider()
                
                # Query interface
                query = st.text_area(
                    "🔍 Ask about the document:",
                    placeholder="e.g., What are the main topics? What's discussed here?",
                    height=100
                )
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("🚀 Get Answer", use_container_width=True):
                        if not query.strip():
                            st.warning("Please enter a question")
                        else:
                            with st.spinner("🤖 Generating answer..."):
                                try:
                                    result = qa({"query": query})
                                    
                                    st.markdown("### 📝 Answer")
                                    st.write(result["result"])
                                    
                                    with st.expander("📚 Source Material"):
                                        for i, doc in enumerate(result.get("source_documents", []), 1):
                                            st.markdown(f"**Reference {i}:**")
                                            st.text(doc.page_content[:400] + "...")
                                            st.caption(f"Page: {doc.metadata.get('page', 'N/A')}")
                                
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
        
        # Clean up temp file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
