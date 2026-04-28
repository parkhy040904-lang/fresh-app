import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.main { background-color: #f0faf0; }
.top-bar {
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    color: white;
    text-align: center;
    padding: 1.2rem;
    border-radius: 0 0 20px 20px;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
}
.greeting {
    text-align: center;
    font-size: 1.1rem;
    color: #388e3c;
    margin-bottom: 1.5rem;
}
.guide-card {
    background: white;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.guide-title { font-weight: bold; font-size: 1rem; color: #2e7d32; margin-bottom: 0.5rem; }
.good { color: #388e3c; }
.bad { color: #e53935; }
.result-box {
    background: white;
    border-radius: 16px;
    padding: 1.2rem;
    margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
.stButton > button {
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem;
    font-size: 1rem;
    font-weight: bold;
    width: 100%;
}
.stButton > button:hover { background: linear-gradient(135deg, #1b5e20, #43a047); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-bar">🌿 Scan Eat!</div>', unsafe_allow_html=True)
st.markdown('<div class="greeting">안녕하세요 👋<br>오늘의 신선도를 확인해볼까요?</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🖼️ 사진 업로드", "📷 카메라로 찍기"])

image = None
image_bytes = None

with tab1:
    uploaded_file = st.file_uploader("갤러리에서 선택 (JPG · PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        image_bytes = uploaded_file.getvalue()

with tab2:
    camera_photo = st.camera_input("카메라로 농산물을 찍어주세요")
    if camera_photo:
        image = Image.open(camera_photo)
        image_bytes = camera_photo.getvalue()

if image:
    st.image(image, caption="선택된 사진", use_container_width=True)
    if st.button("🔍 신선도 분석하기"):
        with st.spinner("AI가 분석 중이에요..."):
            image_data = base64.b64encode(image_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                        {"type": "text", "text": """이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:

농산물 종류:
신선도 점수: (숫자/10)
상태: (신선/보통/주의/부패 중 하나)
상태 설명:
보관 방법:
예상 남은 기한: """}
                    ]
                }]
            )
            result = response.choices[0].message.content
            lines = result.strip().split("\n")

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 📊 분석 결과")
            for line in lines:
                if "농산물 종류" in line:
                    st.markdown(f"🥬 **{line.strip()}**")
                elif "신선도 점수" in line:
                    st.markdown(f"⭐ **{line.strip()}**")
                elif "상태:" in line:
                    val = line.split(":")[-1].strip()
                    if "신선" in val:
                        st.success(f"📊 {line.strip()}")
                    elif "보통" in val:
                        st.warning(f"📊 {line.strip()}")
                    else:
                        st.error(f"📊 {line.strip()}")
                elif "상태 설명" in line:
                    st.info(f"💡 {line.strip()}")
                elif "보관 방법" in line:
                    st.markdown(f"🏪 {line.strip()}")
                elif "예상 남은 기한" in line:
                    st.markdown(f"⏰ {line.strip()}")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📗 농작물 고르는 가이드")

guides = [
    ("🍎 사과", ["껍질 팽팽·광택 있음", "꼭지 싱싱·단단", "달콤한 향"], ["물렁·주름진 것", "검은 반점·곰팡이"]),
    ("🥦 브로콜리", ["짙은 초록색", "꽃봉오리 촘촘히 닫힘", "줄기 단단"], ["노란색 변색", "꽃이 핀 것"]),
    ("🍅 토마토", ["선명한 빨간색", "눌렀을 때 약간 탄력", "꼭지 초록 생기"], ["너무 물렁한 것", "갈라지거나 터진 것"]),
    ("🥕 당근", ["선명한 주황색", "표면 매끄럽고 단단", "잎이 선명한 녹색"], ["갈라지거나 물렁", "흰 줄기 많은 것"]),
    ("🍋 레몬", ["밝고 선명한 노란색", "묵직하고 단단", "향이 진함"], ["초록빛 남아있고 딱딱", "주름 많고 말라있는 것"]),
    ("🫐 블루베리", ["진한 보라-파란색", "흰 분같은 가루 있음", "단단하고 통통함"], ["빨간색 남아있는 것", "물컹하거나 즙 나오는 것"]),
]

for name, good, bad in guides:
    with st.expander(name):
        st.markdown(f'<div class="good">✔ ' + " · ".join(good) + '</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bad">✘ ' + " · ".join(bad) + '</div>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:2rem;">🌱 신선한 농산물로 건강한 하루!</p>', unsafe_allow_html=True)
