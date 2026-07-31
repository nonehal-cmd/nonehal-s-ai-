import streamlit as st
from google import genai
from PIL import Image
import json

# 1. Page Configuration & Wide Grid Layout Setup
st.set_page_config(page_title="Institutional AI Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS aapke sketch/design ke mutabaq colorful boxes aur badges banane ke liye
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

st.title("🛡️ Institutional Pro AI Dashboard")

# Sidebar Configuration
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 Pro-Tip: Yeh engine stable multimodal framework use karta hai.")

# Session States Management
if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_data' not in st.session_state: st.session_state.ai_data = {}

# 2. File Uploaders (Aap chahein toh 1 chart dalein ya 2 combo charts)
col_u1, col_u2 = st.columns(2)
with col_u1: htf_file = st.file_uploader("Upload Image 1 (Higher Timeframe / Main Chart)", type=["jpg", "png", "jpeg"])
with col_u2: ltf_file = st.file_uploader("Upload Image 2 (Lower Timeframe - Optional)", type=["jpg", "png", "jpeg"])

# Preview block
if (htf_file or ltf_file) and not st.session_state.analyzed:
    st.subheader("📸 Uploaded Charts Preview")
    col_img1, col_img2 = st.columns(2)
    if htf_file:
        with col_img1: st.image(Image.open(htf_file), caption="Chart 1", use_container_width=True)
    if ltf_file:
        with col_img2: st.image(Image.open(ltf_file), caption="Chart 2", use_container_width=True)

# Analysis Trigger Button
if htf_file or ltf_file:
    if not st.session_state.analyzed:
        if st.button("🚀 Shuru Karein Deep Live Analysis", use_container_width=True):
            if not api_key:
                st.error("Sidebar me Google Gemini API Key darj karein!")
            else:
                with st.spinner("AI aapke layout ke mutabaq data process kar raha hai..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        contents_list = []
                        if htf_file: contents_list.append(Image.open(htf_file))
                        if ltf_file: contents_list.append(Image.open(ltf_file))
                        
                        prompt = """
                        Aap ek top-tier institutional trader hain. Is chart screenshot ka code-level structure me data chahiye.
                        Mera response strict aur valid JSON format me hona chahiye bina kisi markdown block (```json) ke. 
                        Response is pattern me hona chahiye:
                        {
                            "symbol": "Asset Name / Symbol (e.g. BTC, XAU/USD, RELIANCE)",
                            "full_analysis": "Short 2-line global technical structure statement.",
                            "signal": "BUY ya SELL ya NEUTRAL",
                            "confirmation": "Confirmation percentage (e.g. 85%)",
                            "retail_vs_pro": "Retailer kya sochta hai aur kyun wo galat hai, aur pro logic kya hai.",
                            "liquidity_psychology": "Liquidity sweeps, Support/Resistance zones aur critical psychology points.",
                            "other_news": "Expected macro events, target timeframes aur additional information."
                        }
                        """
                        contents_list.append(prompt)
                        
                        # Standard stable model
                        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=contents_list
                        )
                        
                        clean_text = response.text.strip()
                        if clean_text.startswith("```json"): clean_text = clean_text[7:]
                        if clean_text.endswith("```"): clean_text = clean_text[:-3]
                        
                        st.session_state.ai_data = json.loads(clean_text.strip())
                        st.session_state.analyzed = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error aaya: {str(e)}. Ek baar dobara try karein.")

# 3. Dynamic UI Generation - AAPKE WIREFRAME KE MUTABAQ
if st.session_state.analyzed:
    data = st.session_state.ai_data
    
    if st.button("🔄 Naya Chart Analyze Karein"):
        st.session_state.analyzed = False
        st.session_state.ai_data = {}
        st.rerun()

    st.markdown("---")
    
    # ROW 1: SYMBOL | FULL CHART ANALYSIS | SIGNAL | CONF %
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([1.5, 4, 2, 1.5])
    
    with row1_col1:
        st.markdown(f"<div class='header-box'><span style='color:#00FFCC;'>SYMBOL</span><br><span style='font-size:20px;'>{data.get('symbol', 'N/A')}</span></div>", unsafe_allow_html=True)
        
    with row1_col2:
        st.markdown(f"<div class='header-box' style='text-align:left;'><span style='color:#00FFCC;'>FULL CHART ANALYSIS</span><br><span style='font-weight:normal;'>{data.get('full_analysis', 'N/A')}</span></div>", unsafe_allow_html=True)
        
    with row1_col3:
        sig = data.get('signal', 'NEUTRAL').upper()
        bg_class = "signal-buy" if "BUY" in sig else ("signal-sell" if "SELL" in sig else "header-box")
        st.markdown(f"<div class='{bg_class}'>SIGNAL<br>{sig}</div>", unsafe_allow_html=True)
        
    with row1_col4:
        st.markdown(f"<div class='conf-circle'>{data.get('confirmation', '50%')}</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2: IMAGE SIDES & MULTI-GRID BOXES
    main_col1, main_col2, main_col3 = st.columns([2.5, 4.5, 4])
    
    with main_col1:
        st.markdown("<p style='font-weight:bold; color:#777;'>📸 CHARTS PREVIEW</p>", unsafe_allow_html=True)
        if htf_file: st.image(Image.open(htf_file), caption="Main Image", use_container_width=True)
        if ltf_file: st.image(Image.open(ltf_file), caption="Secondary Image", use_container_width=True)
        
    with main_col2:
        st.markdown(f"""
            <div class='content-card'>
                <h4 style='color:#FF4B4B;'>🧠 Retail vs Pro Logic (Sabse Alag)</h4>
                <p>{data.get('retail_vs_pro', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='psych-card'>
                <h4 style='color:#00FFCC;'>📊 Liquidity, Levels & Psychology</h4>
                <p>{data.get('liquidity_psychology', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with main_col3:
        st.markdown(f"""
            <div class='content-card' style='border-top: 4px solid #9900FF; min-height:535px;'>
                <h4 style='color:#9900FF;'>📰 Other, News & Macro Events</h4>
                <p>{data.get('other_news', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
