import streamlit as st
from PIL import Image
import json, base64, requests, io

st.set_page_config(page_title="Groq AI Dashboard", layout="wide")

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

st.title("🟢 Groq Llama-3 AI Chart Dashboard")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_data' not in st.session_state: st.session_state.ai_data = {}

col_u1, col_u2 = st.columns(2)
with col_u1: htf_file = st.file_uploader("Upload Main Chart Image", type=["jpg", "png", "jpeg"])
with col_u2: ltf_file = st.file_uploader("Upload Secondary Image (Optional)", type=["jpg", "png", "jpeg"])

if htf_file or ltf_file:
    if not st.session_state.analyzed:
        if st.button("🚀 Shuru Karein Deep Live Analysis", use_container_width=True):
            if not api_key:
                st.error("Kripya Groq API Key dalein!")
            else:
                with st.spinner("Groq Llama AI data process kar raha hai..."):
                    try:
                        main_img = Image.open(htf_file if htf_file else ltf_file)
                        if main_img.mode in ("RGBA", "P"): main_img = main_img.convert("RGB")
                        
                        buffered = io.BytesIO()
                        main_img.save(buffered, format="JPEG")
                        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        
                        prompt = 'Aap ek top-tier institutional trader hain. strict aur valid JSON format me bina kisi markdown block ke response dein: {"symbol": "Asset Name", "full_analysis": "Short statement", "signal": "BUY/SELL/NEUTRAL", "confirmation": "85%", "retail_vs_pro": "details", "liquidity_psychology": "details", "other_news": "details"}'
                        
                        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                        payload = {
                            "model": "llama-3.2-11b-vision-preview",
                            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}],
                            "response_format": {"type": "json_object"}
                        }
                        res = requests.post("https://groq.com", headers=headers, json=payload)
                        clean_text = res.json()['choices']['message']['content'].strip().replace("```json", "").replace("```", "")
                        
                        st.session_state.ai_data = json.loads(clean_text.strip())
                        st.session_state.analyzed = True
                        st.rerun()
                    except Exception as e: st.error(f"Error: {str(e)}")

# Display UI Structure (Same layout)
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
    with m2:
        st.markdown(f"<div class='content-card'><h4 style='color:#FF4B4B;'>🧠 Retail vs Pro Logic</h4><p>{data.get('retail_vs_pro', 'N/A')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='psych-card'><h4 style='color:#00FFCC;'>📊 Liquidity & Psychology</h4><p>{data.get('liquidity_psychology', 'N/A')}</p></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='content-card' style='border-top: 4px solid #9900FF; min-height:535px;'><h4 style='color:#9900FF;'>📰 Other & News</h4><p>{data.get('other_news', 'N/A')}</p></div>", unsafe_allow_html=True)
