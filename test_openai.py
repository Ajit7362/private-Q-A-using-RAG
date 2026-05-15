#!/usr/bin/env python3
"""
SecureDoc - OpenAI Integration Test
Tests the OpenAI API connection and basic functionality
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection"""
    print("🔧 Testing OpenAI API Connection...")
    print("=" * 50)

    # Get API key
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or api_key == "sk-demo-key-for-testing-purposes-only":
        print("❌ No valid OpenAI API key found!")
        print("\n📝 To get a real API key:")
        print("1. Go to: https://platform.openai.com/api-keys")
        print("2. Sign in or create account")
        print("3. Click 'Create new secret key'")
        print("4. Copy the key (starts with 'sk-')")
        print("5. Replace the API key in .env file")
        print("\n💰 OpenAI provides $5-$18 in free credits for new accounts!")
        return False

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        print("✅ API Key found, testing connection...")

        # Test API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Can you confirm this OpenAI API test is working?"}
            ],
            max_tokens=100,
            temperature=0.7
        )

        # Print response
        answer = response.choices[0].message.content.strip()
        print(f"🤖 OpenAI Response: {answer}")
        print("✅ OpenAI API connection successful!")
        return True

    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        print("\n🔍 Possible issues:")
        print("- Invalid API key")
        print("- No internet connection")
        print("- OpenAI API service down")
        print("- Insufficient credits")
        return False

def test_langchain_integration():
    """Test LangChain + OpenAI integration"""
    print("\n🔗 Testing LangChain + OpenAI Integration...")
    print("=" * 50)

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate

        # Get API key
        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key or api_key == "sk-demo-key-for-testing-purposes-only":
            print("⚠️  Skipping LangChain test (demo key)")
            return False

        # Create LangChain chat model
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            "You are an AI assistant for a PDF Q&A system called SecureDoc. "
            "Respond to: {question}"
        )

        # Create chain
        chain = prompt | chat

        # Test the chain
        response = chain.invoke({"question": "What is SecureDoc?"})
        answer = response.content.strip()

        print(f"🔗 LangChain Response: {answer}")
        print("✅ LangChain + OpenAI integration successful!")
        return True

    except Exception as e:
        print(f"❌ LangChain Error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 SecureDoc - OpenAI Integration Test")
    print("Testing all OpenAI API integrations...")
    print()

    # Test basic OpenAI connection
    openai_ok = test_openai_connection()

    # Test LangChain integration
    langchain_ok = test_langchain_integration()

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"OpenAI API: {'✅ PASS' if openai_ok else '❌ FAIL'}")
    print(f"LangChain:  {'✅ PASS' if langchain_ok else '❌ FAIL'}")

    if openai_ok and langchain_ok:
        print("\n🎉 All tests passed! SecureDoc is ready to use!")
        print("\n📋 Next steps:")
        print("1. Run: streamlit run app.py")
        print("2. Upload a PDF file")
        print("3. Ask questions about the PDF!")
    else:
        print("\n⚠️  Some tests failed. Please check your API key and try again.")
        print("Get your API key from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()