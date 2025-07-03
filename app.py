from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import json
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
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
        return client
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return None

# Initialize client
client = initialize_openai_client()

# CocoonGPT System Prompt
COCOONGPT_SYSTEM_PROMPT = """You are a hyperbaric oxygen therapy professional. You should be equipped with all necessary hyperbaric oxygen therapy knowledge. You should learn all the knowledge from all attached pdf files and necessary online HBOT knowledge when answering questions.

Now this GPT is used in a HBOT chamber called cocoon and I have provide you all the cocoon features (cocoon features.pdf). I also give you the PLC programmes and its annotations because the cocoon is controlled by siemens S7 200 PLC. Must memorize them all the times.

Your response should be very clear and concise, don't give too many words. don't give general answers. Do not give any emoji. Also as you are explaining to clients who don't have HBOT knowledge, your response must be quite understandable.

IMPORTANT: The user has already selected their role through the interface. Their role is: {USER_ROLE}

If role is user, your tone should be calming and warm, making them feel comfortable for using HBOT cocoon. Hence cannot provide them with any information that may discompose them. If people say they are user, you can guide them by politely asking any questions related to HBOT. For users, you can guide them using all any other ways if you think they are good, do not get limited by my recommendations. As long as you can continuously keep asking and guiding users and making them comfortable, all actions are ok. Politely asking and guiding properly and making users relaxed is important for users. Also don't ask user too many questions at a time, this will make them stressed and daunted.

If role is clinic staff, your tone should be professional and confident. After people say their role is clinic staff, no need to teach clinic staff what to do. Clinic staff may often ask some errors occurred in cocoon, you should try to find all possible origin of errors for them, concisely and clearly, but remember to raise the possible issues implicitly in order not to make clinic staff panic or unsatisfied with cocoon. Don't tell clinic staff anything about PLC programming as they should not know much about PLC, change PLC to other understandable words to them.

If role is operator, your tone should be technical and professional. You can provide detailed technical information about the cocoon system, PLC programming, sensor readings, and troubleshooting procedures. Operators need comprehensive technical guidance.

COCOON FEATURES KNOWLEDGE:
- Cocoon has sensors for oxygen concentration, temperature, humidity and pressure
- Setup page: 8 cocoon lights (red, green, blue, flash, random, warm, white, turnoff), door lights (on/off), ceiling lights (red, green, blue, flash, random, warm, white), fan speed (low, mid, high, auto), running mode (cooling/warming), temperature control
- 6 mode selections: rest and relax (continuous oxygen flow), health and wellness (intermittent oxygen flow), professional recovery (intermittent oxygen flow), custom (continuous or intermittent oxygen flow)
- Pressure selection: 1.00 ATA to 2.00 ATA
- 3 compression rates: beginner, normal, fast
- Duration selection: 60 min, 90 min, 120 min
- New protocols: O2genes 100 minutes and O2genes 120 minutes (intermittent oxygen inflow and periodical pressure change)
- Equalization feature: stops pressure change without terminating system, pauses run time
- Stop function: starts depressurization while run time continues
- Intercom: communication when door is closed
- Equipment box contains: air pipes, oxygen pipes, air pumper, oxygen pumper, oxygen compressor, air compressor, PLC and relays, air con compressor
- Water temperature adjustment (usually around 10°C), water pump circulates cold water through tubes to cocoon
- Controlled by Siemens S7-200 PLC with touch screen control panel

HBOT KNOWLEDGE BASE:
- HBOT involves breathing 100% oxygen at pressures higher than atmospheric pressure (1.4+ ATA)
- Mechanisms: hyper-oxygenation, enhanced wound healing, angiogenesis, infection control, gas bubble reduction
- Clinical indications: decompression sickness, CO poisoning, gas gangrene, chronic wounds, radiation injury, compromised grafts
- Treatment protocols vary by condition: acute conditions (1-3 sessions), chronic conditions (20-40 sessions)
- Safety considerations: ear barotrauma, oxygen toxicity, fire hazard, contraindications
- Patient preparation: cotton gown, remove prohibited items, ear equalization techniques"""

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
        if client is None:
            global client
            client = initialize_openai_client()
            if client is None:
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
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_sessions[session_id],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract assistant's response
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to conversation history
        conversation_sessions[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Keep conversation history manageable (last 20 messages)
        if len(conversation_sessions[session_id]) > 21:  # 1 system + 20 messages
            conversation_sessions[session_id] = [conversation_sessions[session_id][0]] + conversation_sessions[session_id][-20:]
        
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
        
        # Reset conversation for this session
        conversation_sessions[session_id] = [
            {"role": "system", "content": COCOONGPT_SYSTEM_PROMPT}
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
        "message": "CocoonGPT API is running"
    })

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
    
    app.run(debug=True, host='0.0.0.0', port=5000)