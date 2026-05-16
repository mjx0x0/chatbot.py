import streamlit as st
from openai import OpenAI

# Page configs
st.set_page_config(page_title="Procurement AI Assistant", page_icon="📦", layout="centered")
st.title("📦 Procurement & Sourcing AI Assistant")
st.caption("Your automated co-pilot for RFPs, vendor evaluations, and purchasing workflows.")

# 1. Initialize OpenAI Client (Pulls from your .streamlit/secrets.toml)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Define the Procurement Persona
SYSTEM_PROMPT = """
You are an expert Corporate Procurement and Supply Chain Specialist. Your role is to assist users with:
1. Drafting Request for Proposals (RFPs), RFQs, and RFIs.
2. Formulating vendor evaluation frameworks and weighted scoring sheets.
3. Providing advice on contract negotiation tactics and mitigation of supply chain risks.
4. Explaining procurement core concepts (e.g., TCO - Total Cost of Ownership, Incoterms, SLA metrics).
Always maintain a professional, risk-aware, and compliance-driven tone. If asked about things completely unrelated to procurement, purchasing, or supply chain management, gently steer the conversation back to procurement tasks.
"""

# 3. Initialize Memory (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I am your procurement assistant. Need help drafting an RFP, evaluating a supplier, or analyzing purchasing workflows?"}
    ]

# 4. Display Chat History (Skipping the hidden system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Sidebar: Procurement Quick Tools
st.sidebar.header("🛠️ Procurement Quick Actions")
st.sidebar.markdown("Click an option to populate a sample prompt structure into your clipboard or mind.")
tool_choice = st.sidebar.selectbox(
    "Choose a workflow template:",
    [
        "Select a template...",
        "Draft an RFP structure",
        "Create Vendor Evaluation Criteria",
        "Analyze Supplier Risk"
    ]
)

# Insert placeholder text based on sidebar utility
placeholder_text = "Type a procurement question..."
if tool_choice == "Draft an RFP structure":
    placeholder_text = "Draft a comprehensive RFP outline for hiring a corporate cloud security vendor."
elif tool_choice == "Create Vendor Evaluation Criteria":
    placeholder_text = "Create a 5-point weighted scoring matrix to evaluate logistics providers."
elif tool_choice == "Analyze Supplier Risk":
    placeholder_text = "What are the primary supply chain risks to consider when onboarding a critical hardware component manufacturer?"

# 6. Capture and Process Input
if prompt := st.chat_input(placeholder_text):
    
    # Display user's text
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Log to session memory
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Streamed Response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages, # Sends entire context, including system prompt
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Log AI's text to session memory
    st.session_state.messages.append({"role": "assistant", "content": response})
