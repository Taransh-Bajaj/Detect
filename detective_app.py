import streamlit as st
import random
import os
import time
from dotenv import load_dotenv
from groq import Groq

# 1. INITIAL SETUP
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Detective: INVESTIGATE THE CRIMINAL", page_icon="🕵️", layout="wide")

# Custom Cyber-styling for Gurugram 2077
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ffcc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #7000ff); color: white; 
        border: none; border-radius: 5px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00f2ff; }
    .case-box { padding: 20px; border: 2px solid #7000ff; border-radius: 10px; background: #161b22; margin-bottom: 20px; }
    .chat-bubble { padding: 12px; border-radius: 8px; margin-bottom: 8px; background: #21262d; border-left: 4px solid #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'bounty' not in st.session_state:
    st.session_state.bounty = 100
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_brief' not in st.session_state:
    st.session_state.current_brief = ""

# 3. GAME ENGINE FUNCTIONS
def start_new_case():
    st.session_state.game_active = True
    st.session_state.chat_history = []
    
    # Gurugram 2077 Scenarios
    crimes = ["50 Lakhs in Crypto stolen", "A high-end Cyber-Processor missing", "Private database breached", "A luxury Ferrari hover-car hijacked"]
    locations = ["Cyber Hub", "Sector 29", "The DLF Phase V Tower", "A basement in Old Gurgaon", "Ambience Mall Rooftop"]
    
    st.session_state.current_brief = f"🚨 CASE REPORT: {random.choice(crimes)} from {random.choice(locations)}."
    
    # Setup Suspects
    names = ["Suspect A", "Suspect B", "Suspect C"]
    liar_index = random.randint(0, 2)
    st.session_state.suspects = {}
    
    for i, name in enumerate(names):
        st.session_state.suspects[name] = {
            "is_liar": (i == liar_index),
            "alibi": random.choice(["I was at a party in Sector 44", "I was sleeping at home", "I was working late at the office", "I was stuck in a traffic jam at the toll"]),
            "job": random.choice(["Software Dev", "Data Broker", "Street Mechanic", "Corporate Manager"])
        }

# 4. SIDEBAR HUD
with st.sidebar:
    st.title("🆔 POLICE TERMINAL")
    st.metric("💰 BOUNTY", f"{st.session_state.bounty} CR")
    
    if st.button("📂 GENERATE NEW CASE"):
        start_new_case()
        st.rerun()

    st.divider()
    st.subheader("🛠️ INVESTIGATOR TOOLS")
    
    if st.button("🔍 AI LIE DETECTOR (50 CR)"):
        if st.session_state.bounty >= 50 and st.session_state.chat_history:
            st.session_state.bounty -= 50
            # Check last suspect message for "deception"
            st.toast("📡 Analyzing biometric voice stress...")
            time.sleep(1)
            # Secretly find if the liar spoke last
            prob = random.randint(75, 98) if any(s['is_liar'] for s in st.session_state.suspects.values() if s['is_liar']) else random.randint(10, 35)
            st.info(f"Deception Probability: {prob}%")
        elif not st.session_state.chat_history:
            st.warning("No data to analyze.")
        else:
            st.error("Need 50 CR!")

    if st.button("🔓 DATA BREACH (30 CR)"):
        if st.session_state.bounty >= 30:
            st.session_state.bounty -= 30
            target = random.choice(list(st.session_state.suspects.keys()))
            job = st.session_state.suspects[target]['job']
            st.warning(f"🔓 LEAK: {target} is actually a {job}.")
        else:
            st.error("Need 30 CR!")

# 5. MAIN GAME UI
st.title("🌆 GURUGRAM 2077: CRIME DIVISION")

if st.session_state.game_active:
    # Display the Brief
    st.markdown(f"<div class='case-box'><h4>{st.session_state.current_brief}</h4></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 INTERROGATION LOG")
        for chat in st.session_state.chat_history:
            role_label = "🕵️ YOU" if chat['role'] == "user" else "👤 TARGET"
            st.markdown(f"<div class='chat-bubble'><strong>{role_label}:</strong> {chat['content']}</div>", unsafe_allow_html=True)

        user_input = st.text_input("Talk to A, B, or C:", placeholder="Ask where they were...")
        
        if st.button("SEND ⚡"):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # REFINED NATURAL BRAIN
                prompt = f"""
                You are playing characters in a mystery game set in Gurugram 2077.
                CASE: {st.session_state.current_brief}
                SUSPECTS: {st.session_state.suspects}
                
                STRICT RULES:
                1. Speak naturally like a normal person (no heavy sci-fi slang).
                2. If you are the LIAR, be defensive and stick to your alibi.
                3. If you are INNOCENT, be slightly annoyed but honest.
                4. Do NOT use the words 'truth', 'liar', or 'innocent'.
                5. Respond only as the suspect(s) mentioned in the user's question.
                """
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_input}]
                )
                
                st.session_state.chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
                st.rerun()

    with col2:
        st.subheader("⚖️ VERDICT")
        suspect_choice = st.radio("Who is the Liar?", ["Suspect A", "Suspect B", "Suspect C"])
        
        if st.button("🚨 ARREST"):
            if st.session_state.suspects[suspect_choice]['is_liar']:
                st.session_state.bounty += 100
                st.balloons()
                st.success(f"CASE CLOSED! {suspect_choice} was guilty. +100 CR.")
                st.session_state.game_active = False
            else:
                st.session_state.bounty -= 50
                st.error(f"BLUNDER! {suspect_choice} was innocent. -50 CR.")
                st.session_state.game_active = False

else:
    st.info("👈 Use the terminal on the left to start a new investigation.")

st.divider()
st.caption("Detective Game | Developed by Taransh Bajaj")