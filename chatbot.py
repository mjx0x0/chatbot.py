import streamlit as st
import time

# Page configs
st.set_page_config(page_title="Procurement AI Assistant", page_icon="📦", layout="centered")
st.title("📦 Procurement & Sourcing AI Assistant")
st.caption("Your automated co-pilot for RFPs, vendor evaluations, and purchasing workflows.")

# 1. Define the Procurement Persona (Kept for systemic consistency if you link another LLM later)
SYSTEM_PROMPT = """
You are an expert Corporate Procurement and Supply Chain Specialist. Your role is to assist users with:
1. Drafting Request for Proposals (RFPs), RFQs, and RFIs.
2. Formulating vendor evaluation frameworks and weighted scoring sheets.
3. Providing advice on contract negotiation tactics and mitigation of supply chain risks.
4. Explaining procurement core concepts (e.g., TCO - Total Cost of Ownership, Incoterms, SLA metrics).
Always maintain a professional, risk-aware, and compliance-driven tone.
"""

# 2. Initialize Memory (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I am your procurement assistant. Need help drafting an RFP, evaluating a supplier, or analyzing purchasing workflows?"}
    ]

# 3. Display Chat History (Skipping the hidden system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Sidebar: Procurement Quick Tools
st.sidebar.header("🛠️ Procurement Quick Actions")
st.sidebar.markdown("Click an option to populate a sample prompt structure into your mind.")
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

# 5. Native Response Simulator (Simulates an LLM streaming text)
def simulate_procurement_response(user_input):
    # Custom automated replies based on what the user selects or types
    if "rfp" in user_input.lower():
        text = "### 📋 Draft RFP Framework\n1. **Executive Summary**: Project scope and goals.\n2. **Statement of Work (SOW)**: Technical requirements.\n3. **Timeline**: Milestone expectations.\n4. **Submission Guidelines**: Evaluation criteria and deadlines."
    elif "evaluation" in user_input.lower() or "matrix" in user_input.lower():
        text = "### ⚖️ Supplier Evaluation Metrics\n- **Technical Capability (35%)**: Skillset match.\n- **Cost & Commercial Terms (30%)**: Price competitiveness.\n- **Risk & Compliance (20%)**: Legal and financial health.\n- **SLA & Support (15%)**: Responsiveness and uptime."
    else:
        text = f"Thank you for your procurement request regarding: *'{user_input}'*. I am processing this workflow simulation according to established compliance standards."
    
    # Yield individual words to simulate streaming text
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.08)

# 6. Capture and Process Input
if prompt := st.chat_input(placeholder_text):
    
    # Display user's text
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Log to session memory
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Streamed Local Response
    with st.chat_message("assistant"):
        # st.write_stream natively animates python generators/streams
        response = st.write_stream(simulate_procurement_response(prompt))
    
    # Log simulated text to session memory
    st.session_state.messages.append({"role": "assistant", "content": response})
