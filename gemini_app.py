import streamlit as st
from google import genai
from PIL import Image
import json

st.set_page_config(page_title="Gemini AI Dashboard", layout="wide")

st.markdown("""
    <style>
    .header-box { background-color: #1E1E1E; padding: 15px; border-radius: 8px; border: 1px solid #333; text-align: center; font-weight: bold; }
    .signal-buy { background-color: #155724; color: #d4edda; padding: 15px; border-radius: 8px; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #28a745; }
    .signal-sell { background-color: #721c24; color: #f8d7da; padding: 15px; border-radius: 8px; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #dc3545; }
    .conf-circle { background-color: #004085; color: #cce5ff; padding: 15px; border-radius: 50%; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #004085; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: auto; }
    .content-card { background-color: #121212; padding: 20px; border-radius: 10px; border-top: 4px solid #00FFCC; min-height: 250px; margin-bottom: 15px; }
    .psych-card { background-color: #121212; padding: 20px; border-radius: 10px; border-top: 4px solid #FFCC00; min-height: 250px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔵 Gemini Pro AI Chart Dashboard")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_data' not in st.session_state: st.session_state.ai_data = {}

col_u1, col_u2 = st.columns(2)
with col_u1: htf_file = st.file_uploader("Upload Image 1", type=["jpg", "png", "jpeg"])
with col_u2: ltf_file = st.file_uploader("Upload Image 2 (Optional)", type=["jpg", "png", "jpeg"])

if htf_file or ltf_file:
    if not st.session_state.analyzed:
        if st.button("🚀 Shuru Karein Deep Live Analysis", use_container_width=True):
            if not api_key:
                st.error("Kripya Gemini API Key dalein!")
            else:
                with st.spinner("Gemini AI data process kar raha hai..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        contents_list = []
                        if htf_file: contents_list.append(Image.open(htf_file))
                        if ltf_file: contents_list.append(Image.open(ltf_file))
                        
                        prompt = 'Aap ek top-tier institutional trader hain. strict aur valid JSON format me bina kisi markdown block ke response dein: {"symbol": "Asset Name", "full_analysis": "Short statement", "signal": "BUY/SELL/NEUTRAL", "confirmation": "85%", "retail_vs_pro": "details", "liquidity_psychology": "details", "other_news": "details"}'
                        contents_list.append(prompt)
                        
                        response = client.models.generate_content(model='gemini-2.0-flash', contents=contents_list)
                        clean_text = response.text.strip().replace("```json", "").replace("```", "")
                        st.session_state.ai_data = json.loads(clean_text.strip())
                        st.session_state.analyzed = True
                        st.rerun()
                    except Exception as e: st.error(f"Error: {str(e)}")

# Display UI Structure
if st.session_state.analyzed:
    data = st.session_state.ai_data
    if st.button("🔄 Naya Chart Analyze Karein"):
        st.session_state.analyzed = False; st.session_state.ai_data = {}; st.rerun()
    
    st.markdown("---")
    r1, r2, r3, r4 = st.columns([1.5, 4, 2, 1.5])
    with r1: st.markdown(f"<div class='header-box'><span style='color:#00FFCC;'>SYMBOL</span><br><span>{data.get('symbol','N/A')}</span></div>", unsafe_allow_html=True)
    with r2: st.markdown(f"<div class='header-box' style='text-align:left;'><span style='color:#00FFCC;'>FULL ANALYSIS</span><br>{data.get('full_analysis','N/A')}</div>", unsafe_allow_html=True)
    with r3: 
        sig = data.get('signal', 'NEUTRAL').upper()
        bc = "signal-buy" if "BUY" in sig else ("signal-sell" if "SELL" in sig else "header-box")
        st.markdown(f"<div class='{bc}'>SIGNAL<br>{sig}</div>", unsafe_allow_html=True)
    with r4: st.markdown(f"<div class='conf-circle'>{data.get('confirmation', '50%')}</div>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns([2.5, 4.5, 4])
    with m1:
        if htf_file: st.image(Image.open(htf_file), use_container_width=True)
        if ltf_file: st.image(Image.open(ltf_file), use_container_width=True)
    with m2:
        st.markdown(f"<div class='content-card'><h4 style='color:#FF4B4B;'>🧠 Retail vs Pro Logic</h4><p>{data.get('retail_vs_pro', 'N/A')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='psych-card'><h4 style='color:#00FFCC;'>📊 Liquidity & Psychology</h4><p>{data.get('liquidity_psychology', 'N/A')}</p></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='content-card' style='border-top: 4px solid #9900FF; min-height:535px;'><h4 style='color:#9900FF;'>📰 Other & News</h4><p>{data.get('other_news', 'N/A')}</p></div>", unsafe_allow_html=True)
