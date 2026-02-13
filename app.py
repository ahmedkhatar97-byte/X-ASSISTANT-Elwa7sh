import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
from streamlit_mic_recorder import mic_recorder

# 1. الهوية والذاكرة
st.set_page_config(page_title="X Assistant V2", page_icon="🤖")
st.title("🤖 X Assistant V2")
st.markdown("تطوير المبرمج: **أحمد الحريف**")

# 2. تفعيل مفتاح السحر اللي بعته
genai.configure(api_key="AIzaSyDKPuAj8fjSvp5ykmHeyKGRpUSO-V6fTVE")

# 3. القائمة الجانبية
st.sidebar.title("إعدادات Harreef 😎")
uploaded_file = st.sidebar.file_uploader("📸 ابعت صورة للمساعد:", type=["jpg", "png", "jpeg"])

# وظيفة الصوت
def speak(text):
    try:
        tts = gTTS(text=text, lang='ar')
        tts.save("voice.mp3")
        st.audio("voice.mp3", format='audio/mp3', autoplay=True)
    except:
        pass

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. إدخال الصوت والنص
st.write("🎤 سجل صوتك يا حريف:")
audio_data = mic_recorder(start_prompt="دوس وابدأ كلام", stop_prompt="ارسل الطلب", key='recorder')
prompt = st.chat_input("اسأل X Assistant V2...")

if prompt or audio_data:
    user_input = prompt if prompt else "حلل اللي سمعته أو اللي شايفه في الصورة"
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        # تعليمات الشخصية (زي ما طلبت بالظبط)
        sys_msg = "أنت X Assistant V2، مبرمجك أحمد الحريف. رد بالعامية المصرية بطلاقة وناديه يا حريف أو يا أحمد."
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            response = model.generate_content([f"{sys_msg} {user_input}", img])
        else:
            response = model.generate_content(f"{sys_msg} {user_input}")
            
        res_text = response.text
        st.markdown(res_text)
        speak(res_text) # المساعد هينطق الرد
        st.session_state.messages.append({"role": "assistant", "content": res_text})
      
