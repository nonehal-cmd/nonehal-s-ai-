import streamlit as st
from PIL import Image
import json, base64, io
from groq import Groq

# Page Config aapke design layout ke mutabaq wide view me
st.set_page_config(page_title="Groq AI Dashboard", layout="wide")

# Custom CSS for Professional Layout
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

st.title("🟢 Groq Llama AI Chart Dashboard")

# Sidebar for Key Input
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 Groq Engine fast vision models use karta hai jo bilkul free hain.")

if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_data' not in st.session_state: st.session_state.ai_data = {}

# File uploaders
col_u1, col_u2 = st.columns(2)
with col_u1: htf_file = st.file_uploader("Upload Image 1 (Main Chart)", type=["jpg", "png", "jpeg"])
with col_u2: ltf_file = st.file_uploader("Upload Image 2 (Optional)", type=["jpg", "png", "jpeg"])

if htf_file or ltf_file:
    if not st.session_state.analyzed:
        if st.button("🚀 Shuru Karein Deep Live Analysis", use_container_width=True):
            if not api_key:
                st.error("Kripya Sidebar me Groq API Key dalein!")
            else:
                with st.spinner("Groq Llama AI saare live vision models test kar raha hai..."):
                    try:
                        # Image conversion
                        main_img = Image.open(htf_file if htf_file else ltf_file)
                        if main_img.mode in ("RGBA", "P"): 
                            main_img = main_img.convert("RGB")
                        
                        buffered = io.BytesIO()
                        main_img.save(buffered, format="JPEG")
                        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        data_url = f"data:image/jpeg;base64,{base64_image}"
                        
                        prompt = """
                        You are a top-tier institutional market analyst. Analyze this chart screenshot and respond STRICTLY in a valid JSON format. Do NOT wrap your response in markdown code blocks. Your output must strictly match this exact JSON schema:
                        {
                            "symbol": "Asset Name / Trading Pair",
                            "full_analysis": "Provide a clean 2-line global macro/technical market structure statement.",
                            "signal": "BUY or SELL or NEUTRAL",
                            "confirmation": "Confidence level percentage like 85%",
                            "retail_vs_pro": "Explain what a typical retail trader thinks here, why they are wrong, and what the professional institutional logic is.",
                            "liquidity_psychology": "Identify liquidity sweeps, invalidation levels, crucial support/resistance targets, and psychological zones.",
                            "other_news": "Detail any upcoming economic indicators, relevant macro news, timeframes, or additional information."
                        }
                        """
                        
                        client = Groq(api_key=api_key)
                        
                        # 🚨 MULTI-MODEL FALLBACK TRIPLE PROTECTION SYSTEM
                        models_to_test = [
                            "llama-3.2-90b-vision-preview",
                            "llama-3.2-11b-vision-preview",
                            "llama-3.2-11b-vision",
                            "llava-v1.5-7b-preview"
                        ]
                        
                        response = None
                        last_error = ""
                        
                        for current_model in models_to_test:
                            try:
                                response = client.chat.completions.create(
                                    model=current_model,
                                    messages=[
                                        {
                                            "role": "user", 
                                            "content": [
                                                {"type": "text", "text": prompt}, 
                                                {"type": "image_url", "image_url": {"url": data_url}}
                                            ]
                                        }
                                    ],
                                    response_format={"type": "json_object"}
                                )
                                # Agar response bina error ke mil gaya toh loop tod do
                                if response:
                                    break
                            except Exception as e:
                                last_error = str(e)
                                continue # Agle model par jao
                        
                        if response is None:
                            raise Exception(f"Groq ke saare vision models offline hain ya decommissioned hain. Last Server Error: {last_error}")
                            
                        clean_text = response.choices.message.content.strip()
                        
                        if clean_text.startswith("```json"): clean_text = clean_text[7:]
                        if clean_text.startswith("```"): clean_text = clean_text[3:]
                        if clean_text.endswith("```"): clean_text = clean_text[:-3]
                        
                        st.session_state.ai_data = json.loads(clean_text.strip())
                        st.session_state.analyzed = True
                        st.rerun()
                            
                    except Exception as e: 
                        st.error(f"Dikkat aayi: {str(e)}")

# Display UI Structure (Symmetric Dashboard)
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
