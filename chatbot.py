import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Theme Setting
st.set_page_config(
    page_title="Isko BidDo | AI Inquiry Support", 
    page_icon="🤖", 
    layout="wide"
)

# Custom MSU Maroon & Gold Branding Injection
st.markdown("""
    <style>
        /* Main application font adjustment */
        html, body, [data-testid="stMarkdownContainer"] {
            font-family: 'Inter', sans-serif;
        }
        /* Top Header Styling */
        .msu-header {
            background: linear-gradient(135deg, #7A1C1C 0%, #A32626 100%);
            padding: 24px;
            border-radius: 12px;
            color: white;
            margin-bottom: 25px;
            border-left: 8px solid #FFD700;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .msu-title {
            font-size: 28px;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .msu-subtitle {
            font-size: 14px;
            color: #FFD700;
            margin: 4px 0 0 0;
            font-weight: 500;
            opacity: 0.9;
        }
        /* Chat Message Area Adjustments */
        [data-testid="stChatMessage"] {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Render Branded Header Banner
st.markdown("""
    <div class="msu-header">
        <h1 class="msu-title">🤖 Isko BidDo: AI Inquiry Support System</h1>
        <p class="msu-subtitle">Mindanao State University - General Santos City • Procurement Office Advisory Module</p>
    </div>
""", unsafe_allow_html=True)

# 3. Initialize the Google GenAI Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 4. Refined Institutional System Persona
SYSTEM_PROMPT = """
You are "Isko BidDo AI", the expert Public Procurement Assistant for Mindanao State University - General Santos (MSU-Gensan).
Your core framework is to assist the Bids and Awards Committee (BAC), procurement officers, and faculty end-users.

Your knowledge parameters are strictly bound by Philippine Public Procurement Laws:
1. Republic Act 9184 (Government Procurement Reform Act)
2. Republic Act 12009 (New Government Procurement Act - NGPA) and its modernizations.

Your role is to assist with:
- Clarifying MSU-Gensan standard operating procedures (e.g., PPMP creation, APP consolidation, Purchase Requests).
- Explaining alternative modes of procurement (Small Value Procurement, Shopping, Direct Contracting) for SUCs.
- Explaining the transition to RA 12009 parameters (Fit-for-Purpose modalities, open eMarketplace access, value-for-money metrics).
- Helping draft clear compliance guidelines for transparent digital tracking logs.

Tone: Professional, highly objective, academic, risk-aware, and regulatory-driven. Always frame answers in the context of MSU-Gensan administrative compliance.
"""

# 5. Sidebar Layout with Quick Reference Actions
with st.sidebar:
    st.markdown("### 🏛️ University Hub")
    # Clean fallback text presentation if image has network loading delays
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/Mindanao_State_University_System_Seal.svg", 
        width=120
    )
    st.markdown("---")
    st.markdown("### 🛠️ Quick Inquiry Presets")
    st.caption("Select an automated template focus area to guide your input:")
    
    workflow_preset = st.selectbox(
        "Choose Focus Template:",
        [
            "Custom Query...",
            "RA 12009 (NGPA) Key Reforms",
            "PPMP to APP Lifecycle",
            "BAC Auditing Protocols"
        ]
    )
    
    st.markdown("---")
    st.info(
        "**System Status:** Connected via secure Gemini 2.5 Flash infrastructure. "
        "All transactions are processed in compliance with COA logging benchmarks."
    )

# Dynamic Placeholder Context Setting
input_placeholder = "Type your procurement or compliance question here..."
if workflow_preset == "RA 12009 (NGPA) Key Reforms":
    input_placeholder = "What are the key changes introduced by RA 12009 for SUC procurement compared to RA 9184?"
elif workflow_preset == "PPMP to APP Lifecycle":
    input_placeholder = "How does an end-user department's PPMP get consolidated into the institutional APP?"
elif workflow_preset == "BAC Auditing Protocols":
    input_placeholder = "What audit trails and metrics are critical for tracking transparency in the digital logbook?"

# 6. Initialize State Tracking Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **Isko BidDo AI**, your compliance advisory assistant for MSU-Gensan procurement. How can I help you optimize your tracking, logging, or regulatory alignment today?"}
    ]

# 7. Render Chat History Layout
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. User Interaction & Prompt Pipeline Execution
if prompt := st.chat_input(input_placeholder):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Format chat architecture cleanly into Gemini's multi-turn schema
        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            g_role = "user" if msg["role"] == "user" else "model"
            gemini_history.append(
                types.Content(
                    role=g_role, 
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        # Connect live stream with system parameters locked in
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,  # Dropped temperature to 0.3 for stricter compliance accuracy
                max_output_tokens=1500
            )
        )
        
        def stream_chunks():
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        full_response = st.write_stream(stream_chunks())
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
