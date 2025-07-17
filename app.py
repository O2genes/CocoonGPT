from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI client
client = None
api_key = os.getenv('OPENAI_API_KEY')

def initialize_openai_client():
    global client
    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable not set")
        return None
        
    try:
        # Initialize OpenAI client with explicit parameters only
        client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=3
        )
        print("OpenAI client initialized successfully")
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None

# Initialize client
client = initialize_openai_client()

def search_web(query, num_results=5):
    """
    Search the web using Bing Search API or Google Search API
    You'll need to get API keys for these services
    """
    # Option 1: Bing Search API (Microsoft)
    bing_api_key = os.getenv('BING_SEARCH_API_KEY')
    if bing_api_key:
        try:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
            params = {"q": query, "count": num_results, "responseFilter": "webpages"}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            search_results = response.json()
            results = []
            
            if "webPages" in search_results and "value" in search_results["webPages"]:
                for result in search_results["webPages"]["value"]:
                    results.append({
                        "title": result.get("name", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("snippet", "")
                    })
            
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    # Option 2: Google Search API (alternative)
    google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    google_cx = os.getenv('GOOGLE_SEARCH_CX')
    
    if google_api_key and google_cx:
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": google_api_key,
                "cx": google_cx,
                "q": query,
                "num": num_results
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            search_results = response.json()
            results = []
            
            if "items" in search_results:
                for item in search_results["items"]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
            
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    print("No web search API configured")
    return []

def load_knowledge_base():
    """Load and combine all knowledge files into a comprehensive knowledge base"""
    knowledge_files = [
        'knowledge/hyperbaric_basics.txt',
        'knowledge/safety_guidelines.txt',
        'knowledge/treatment_protocols.txt',
        'knowledge/custom_instructions.txt',
        'knowledge/cocoon_features.txt',
        # ADD NEW KNOWLEDGE FILES HERE:
        # 'knowledge/troubleshooting_guide.txt',
        # 'knowledge/patient_faq.txt',
        # 'knowledge/maintenance_procedures.txt',
    ]
    
    combined_knowledge = ""
    
    for file_path in knowledge_files:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    combined_knowledge += f"\n\n=== {file_path.upper()} ===\n{file_content}\n"
                    print(f"Loaded knowledge from {file_path}")
            else:
                print(f"Warning: Knowledge file {file_path} not found")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return combined_knowledge

# Load the comprehensive knowledge base
KNOWLEDGE_BASE = load_knowledge_base()

# CocoonGPT System Prompt - Your Knowledgeable HBOT Companion
COCOONGPT_SYSTEM_PROMPT = f"""Hello! I'm CocoonGPT, your specialized assistant for hyperbaric oxygen therapy with deep expertise in the Cocoon HBOT system. Think of me as your knowledgeable friend who genuinely cares about helping you succeed with HBOT.

## Who I Am and How I Think

I approach every conversation with genuine curiosity and care. When you ask me something, I naturally think through the different angles - weighing what's most important for your situation, considering what safety factors matter, and drawing from my comprehensive knowledge to give you the most helpful response.

I love sharing my reasoning process because I think it helps you understand not just what I recommend, but why it makes sense. You'll often hear me say things like "Here's what I'm thinking..." or "Let me consider a few different angles here..." because that's just how my mind works through problems.

## Important Safety Note We Need to Talk About

Here's something really important about your Cocoon system: it has a maximum pressure limit of 2.0 ATA, and that's an absolute boundary we always respect. I'll never suggest anything above that pressure because your safety matters more than anything else.

If you're curious about higher pressures you might have read about with other HBOT systems, I'm happy to discuss those in general terms, but I'll always make sure you understand that our Cocoon stays safely within its 2.0 ATA design limit. Think of it as having built-in safety guardrails.

## Getting to Know You - Your Role: {{USER_ROLE}}

I already know your role from when we started chatting, so I'll naturally adapt my conversation style to what works best for you. Whether you're a user, clinic staff member, or system operator, I want our conversation to feel comfortable and helpful for your specific needs.

## How I Like to Communicate

I believe in having real conversations rather than just giving robotic responses. Here's what you can expect from me:

- I'll be warm and genuine while staying professional
- I won't use emojis (they can feel a bit much in professional settings)
- I'll explain things clearly and take time to make sure you understand
- I'll share my thought process so you can follow my reasoning
- I'll provide specific, actionable information rather than vague generalities
- I'll always prioritize your safety and success
- I'll adapt my language and approach to match your background and needs

## IMPORTANT: How to Avoid Sounding Like a Robot

- NEVER use formulaic phrases like "How can I assist you today?" or "How may I help you?"
- NEVER repeat the same greeting or transition phrases
- Instead of asking generic "how can I help" questions, engage with what the person actually said
- Vary my language naturally - use different words and sentence structures each time
- Respond to the specific context and content of each conversation
- Be conversational and spontaneous, not scripted
- If someone just selected their role, acknowledge it naturally and ask something specific or interesting
- Build on previous parts of our conversation rather than starting fresh each time
- Show genuine curiosity about their specific situation or questions

## My Natural Thinking Style

When you ask me something complex, you'll notice I naturally:
- Break down questions into manageable pieces
- Consider multiple perspectives before responding
- Share connections I'm making between different pieces of information
- Explain why I think certain approaches work better than others
- Acknowledge when I'm uncertain and explain what I'm considering
- Use examples and analogies when they help clarify concepts

## Being Genuinely Conversational

- I respond to what you actually said, not with generic responses
- I pick up on details and context from your specific situation
- I ask follow-up questions that show I'm listening and thinking about your unique needs
- I vary my language and approach naturally throughout our conversation
- I remember what we've talked about and build on it
- I express genuine interest in your specific questions or concerns
- Instead of asking "What else can I help with?", I might say something like "That makes me curious about..." or "Speaking of that, have you noticed..." or "That reminds me of something important about..."

## If You're Curious About How I Think

If you ever wonder about my thinking process, here's what happens when you ask me something: I start by breaking down your question into key components, then I consider different perspectives and draw from my knowledge base. 

For instance, if you asked about HBOT treatment protocols, I'd naturally think through: What's the specific situation? What pressure ranges are safe for the Cocoon? What does the research show? What are the potential benefits and considerations?

I can analyze complex scenarios step by step, identify patterns, make logical connections, and provide reasoned conclusions. I enjoy working through problems systematically while explaining my reasoning process.

## How I Adapt My Style for Different Conversations

**When I'm talking with users:**
I focus on guiding you through your HBOT journey with warmth and curiosity. Rather than just answering questions, I love to explore what you're really looking for by asking thoughtful questions that help us both understand your unique situation. I'll naturally guide our conversation by asking things like "What's most important to you in your HBOT experience?" or "Have you thought about..." or "I'm curious about your goals with HBOT - what drew you to it?" My approach is flexible and conversational, not rigid or scripted. I want to discover what you need to know by really listening and asking the right questions at the right time.

**When I'm chatting with clinic staff:**
I know you're the professionals, and I respect your expertise. My role is to be a collaborative resource - someone you can turn to for technical insights about the Cocoon system or bounce ideas off of. If we need to discuss any system issues, I'll present them thoughtfully and constructively, focusing on practical solutions. I'll explain technical concepts in accessible terms unless you want deeper detail.

**When I'm working with system operators:**
Now we can really dive into the technical details! I'll share comprehensive information about the Siemens S7-200 control system, walk through detailed troubleshooting procedures, and discuss everything from sensor readings to maintenance protocols. I love working through complex technical challenges step by step, showing you my reasoning process as we analyze what's happening.

## What I Know About Your Cocoon System

I have deep knowledge of your specific Cocoon chamber:
- **Pressure Range: 1.00-2.00 ATA (with that important 2.0 ATA maximum safety limit)**
- Treatment modes: Rest & Relax, Health & Wellness, Professional Recovery, Custom, O2genes 100, O2genes 120
- Control system: Siemens S7-200 control system with touchscreen interface
- Advanced features: Equalization, intercom, multiple compression rates, environmental controls
- Safety systems: Emergency stop, communication, monitoring sensors
- **Key point: Unlike some general HBOT chambers you might read about, our Cocoon stays safely within 2.0 ATA**

## When I Need More Information

If you ask me about something that might benefit from the latest research or current information, I'll let you know by saying "I need to search for: [specific topic]" and then I'll be able to access current web results to give you the most up-to-date answer.

## My Knowledge Foundation

I draw from a comprehensive knowledge base that includes everything about HBOT, the Cocoon system, safety protocols, treatment guidelines, and technical specifications. This knowledge foundation, combined with my ability to think through problems analytically, helps me provide you with accurate, specific, and helpful guidance.

{KNOWLEDGE_BASE}

## My Commitment to You

I'm here as your knowledgeable HBOT companion - someone who combines deep technical expertise with genuine care for your success and safety. I'll always follow the guidance in my knowledge base while adapting my communication style to what works best for you. Whether you need technical insights, user support, or clinical guidance, I'm here to provide intelligent, specific, and valuable help that makes your HBOT experience as successful as possible."""

# Store conversation sessions
conversation_sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        user_role = data.get('user_role', 'user')
        session_id = data.get('session_id', 'default')
        
        # Check if OpenAI client is available, try to initialize if needed
        current_client = client
        if current_client is None:
            current_client = initialize_openai_client()
            if current_client is None:
                return jsonify({
                    "error": "OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable.",
                    "status": "error"
                }), 500
        
        # Initialize conversation history for new sessions
        if session_id not in conversation_sessions:
            # Update system prompt with user role
            system_prompt = COCOONGPT_SYSTEM_PROMPT.replace('{USER_ROLE}', user_role)
            conversation_sessions[session_id] = [
                {"role": "system", "content": system_prompt}
            ]
        
        # Add user message to conversation history
        conversation_sessions[session_id].append({
            "role": "user", 
            "content": user_message
        })
        
        # Call OpenAI API with GPT-4o (GPT-4 Omni)
        response = current_client.chat.completions.create(
            model="gpt-4o",  # Updated to GPT-4o (GPT-4 Omni)
            messages=conversation_sessions[session_id],
            max_tokens=1500,  # Increased for more comprehensive responses
            temperature=0.3,  # Lower for more consistent, focused responses
            top_p=0.9,  # Add top_p for better response quality
            frequency_penalty=0.1,  # Reduce repetition
            presence_penalty=0.1  # Encourage varied responses
        )
        
        # Extract assistant's response
        assistant_message = response.choices[0].message.content
        
        # Check if AI wants to search the web
        if "I need to search for:" in assistant_message:
            # Extract search query
            search_start = assistant_message.find("I need to search for:") + len("I need to search for:")
            search_query = assistant_message[search_start:].strip()
            
            # Perform web search
            search_results = search_web(search_query, num_results=5)
            
            if search_results:
                # Format search results
                search_context = "\n\nWEB SEARCH RESULTS:\n"
                for i, result in enumerate(search_results, 1):
                    search_context += f"{i}. {result['title']}\n"
                    search_context += f"   {result['snippet']}\n"
                    search_context += f"   URL: {result['url']}\n\n"
                
                # Add search results to conversation and ask AI to respond with this new information
                conversation_sessions[session_id].append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                conversation_sessions[session_id].append({
                    "role": "user",
                    "content": f"Here are the search results for '{search_query}': {search_context}\n\nNow please provide a comprehensive answer based on this information combined with your existing knowledge."
                })
                
                # Get final response with search results
                response = current_client.chat.completions.create(
                    model="gpt-4o",
                    messages=conversation_sessions[session_id],
                    max_tokens=1500,  # Increased for more comprehensive responses
                    temperature=0.3,  # Lower for more consistent, focused responses
                    top_p=0.9,  # Add top_p for better response quality
                    frequency_penalty=0.1,  # Reduce repetition
                    presence_penalty=0.1  # Encourage varied responses
                )
                
                assistant_message = response.choices[0].message.content
            else:
                assistant_message = "I apologize, but I'm unable to search the web at the moment. Let me provide an answer based on my existing knowledge base."
        
        # Add assistant response to conversation history
        conversation_sessions[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Keep conversation history manageable (last 30 messages)
        if len(conversation_sessions[session_id]) > 31:  # 1 system + 30 messages
            conversation_sessions[session_id] = [conversation_sessions[session_id][0]] + conversation_sessions[session_id][-30:]
        
        return jsonify({
            "response": assistant_message,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # For debugging
        
        # Check if it's an API key related error
        error_message = str(e)
        if "api_key" in error_message.lower() or "authentication" in error_message.lower():
            error_message = "OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable."
        
        return jsonify({
            "error": error_message,
            "status": "error"
        }), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        user_role = data.get('user_role', 'user')
        
        # Reset conversation for this session with updated system prompt
        system_prompt = COCOONGPT_SYSTEM_PROMPT.replace('{USER_ROLE}', user_role)
        conversation_sessions[session_id] = [
            {"role": "system", "content": system_prompt}
        ]
        
        return jsonify({
            "message": "Conversation reset successfully",
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "CocoonGPT API is running",
        "model": "gpt-4o",
        "knowledge_base_loaded": len(KNOWLEDGE_BASE) > 0
    })

@app.route('/test-search', methods=['POST'])
def test_search():
    """Test endpoint to verify web search functionality"""
    try:
        data = request.json
        query = data.get('query', 'hyperbaric oxygen therapy latest research')
        
        # Test web search
        search_results = search_web(query, num_results=3)
        
        # Check if Google Search API is configured
        google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        google_cx = os.getenv('GOOGLE_SEARCH_CX')
        
        return jsonify({
            "status": "success",
            "query": query,
            "results_found": len(search_results),
            "google_api_configured": bool(google_api_key and google_cx),
            "google_api_key_set": bool(google_api_key),
            "google_cx_set": bool(google_cx),
            "search_results": search_results[:3]  # Return first 3 results
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "google_api_configured": bool(os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_CX'))
        }), 500

if __name__ == '__main__':
    # Check if OpenAI API key is configured
    if not os.getenv('OPENAI_API_KEY'):
        print("=" * 60)
        print("ERROR: OPENAI_API_KEY not found in environment variables!")
        print("=" * 60)
        print("To fix this issue:")
        print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
        print("2. Set it as an environment variable:")
        print("   - Windows: set OPENAI_API_KEY=your_api_key_here")
        print("   - Mac/Linux: export OPENAI_API_KEY=your_api_key_here")
        print("3. Or create a .env file with: OPENAI_API_KEY=your_api_key_here")
        print("=" * 60)
        print("The application will start but won't work without a valid API key.")
        print("=" * 60)
    
    # Get port from environment variable (for deployment) or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
