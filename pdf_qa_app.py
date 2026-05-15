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

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main {
        padding: 2rem
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 SecureDoc - PDF Q&A System")
st.markdown("**Powered by OpenAI GPT + LangChain**")

# Get API key
api_key = os.environ.get("OPENAI_API_KEY")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if api_key:
        st.success("✅ OpenAI API Key configured")
    else:
        st.error("❌ No API Key found")
    
    model = st.selectbox(
        "Model",
        ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=2
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
    st.session_state.pdf_loaded = False

# File uploader
st.divider()
uploaded_file = st.file_uploader("📁 Upload a PDF", type="pdf")

# Load PDF and create QA system
if uploaded_file is not None and not st.session_state.pdf_loaded:
    try:
        # Create temp directory
        temp_dir = tempfile.gettempdir()
        pdf_temp_dir = os.path.join(temp_dir, "securedoc_pdfs")
        os.makedirs(pdf_temp_dir, exist_ok=True)
        
        pdf_path = os.path.join(pdf_temp_dir, uploaded_file.name)
        
        with st.spinner("🔄 Loading and processing PDF..."):
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
                with st.spinner("Creating vector database..."):
                    db = Chroma.from_documents(texts, embeddings)
                    st.session_state.vector_db = db
                
                st.success("✅ Vector database created")
                st.session_state.pdf_loaded = True
        
        # Clean up temp file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        st.info("Please check your PDF file and try again")

# Query interface
st.divider()
st.subheader("🔍 Ask Questions About the PDF")

if st.session_state.vector_db is None:
    st.info("📌 Upload a PDF file first to get started")
else:
    query = st.text_area(
        "Enter your question:",
        placeholder="e.g., What are the main topics?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        search_btn = st.button("🚀 Get Answer", use_container_width=True)
    
    with col2:
        clear_btn = st.button("🔄 Clear", use_container_width=True)
    
    if clear_btn:
        st.session_state.clear()
        st.rerun()
    
    if search_btn:
        if not query.strip():
            st.warning("⚠️ Please enter a question")
        else:
            try:
                with st.spinner("🤖 Generating answer..."):
                    # Create LLM
                    llm = ChatOpenAI(
                        model=model,
                        temperature=temperature,
                        api_key=api_key,
                        max_tokens=1024
                    )
                    
                    # Retrieve documents
                    retriever = st.session_state.vector_db.as_retriever(
                        search_kwargs={"k": 3}
                    )
                    
                    # Get relevant documents
                    docs = retriever.invoke(query)
                    
                    if not docs:
                        st.warning("⚠️ No relevant documents found")
                    else:
                        # Create context from documents
                        context = "\n\n".join([
                            f"Document {i+1}:\n{doc.page_content}"
                            for i, doc in enumerate(docs)
                        ])
                        
                        # Generate answer
                        prompt = f"""Based on the following context from the document, answer the question.

Context:
{context}

Question: {query}

Answer:"""
                        
                        response = llm.invoke(prompt)
                        
                        # Display answer
                        st.markdown("### 📝 Answer")
                        st.write(response.content)
                        
                        # Display sources
                        with st.expander("📚 Source Material"):
                            for i, doc in enumerate(docs, 1):
                                st.markdown(f"**Reference {i}:**")
                                st.text(doc.page_content[:400] + "...")
                                page_num = doc.metadata.get('page', 'N/A')
                                st.caption(f"📖 Page: {page_num}")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please try again or check your API key")

st.divider()
st.markdown("""
### 💡 Tips:
- Ask specific questions about course content
- Questions about objectives, syllabus, grading
- Topics covered, assessment methods
- Or any other syllabus-related queries
""")
