import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; box-sizing: border-box; }
.main { background-color: #f0f0f0; }
#MainMenu, header, footer { visibility: hidden; }

.phone-wrap {
    max-width: 390px;
    margin: 0 auto;
    background: white;
    border-radius: 40px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18);
    padding-bottom: 2rem;
}
.status-bar {
    background: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 1.2rem;
    font-size: 0.75rem;
    font-weight: bold;
}
.app-header {
    background: white;
    text-align: center;
    padding: 0.6rem;
    font-size: 1.1rem;
    font-weight: bold;
    color: #222;
    border-bottom: 1px solid #f0f0f0;
}
.greeting {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    margin: 1rem;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    color: #2e7d32;
    font-size: 0.95rem;
}
.section-card {
    margin: 0.8rem 1rem;
    background: #f9f9f9;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    border: 1px solid #eee;
}
.section-header {
    font-size: 0.82rem;
    color: #888;
    font-weight: bold;
    margin-bottom: 0.7rem;
    letter-spacing: 0.04em;
}
.analyze-wrap { margin: 0.8rem 1rem; }
.stButton > button {
    background: #222 !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    font-weight: bold !important;
    width: 100% !important;
}
.result-section {
    margin: 0.8rem 1rem;
    background: #f9f9f9;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    border: 1px solid #eee;
}
.guide-section { margin: 0.8rem 1rem; }
.guide-title-bar {
    font-weight: bold;
    font-size: 0.95rem;
    color: #222;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.guide-card {
    background: #f9f9f9;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    border: 1px solid #eee;
}
.guide-item-title { font-weight: bold; font-size: 0.92rem; margin-bottom: 0.4rem; }
.good { color: #2e7d32; font-size: 0.85rem; margin-bottom: 0.2rem; }
.bad { color: #e53935; font-size: 0.85rem; }
.footer-bar {
    text-align: center;
    color: #bbb;
    font-size: 0.75rem;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="phone-wrap">', unsafe_allow_html=True)

# 상태바
st.markdown("""
<div class="status-bar">
  <span>9:41</span>
  <span>●●● WiFi 🔋</span>
</div>
""", unsafe_allow_html=True)

# 앱 헤더
st.markdown('<div class="app-header">🌿 Scan Eat!</div>', unsafe_allow_html=True)

# 인사
st.markdown("""
<div class="greeting">
  안녕하세요 👋<br>오늘의 신선도를 확인해볼까요?
</div>
""", unsafe_allow_html=True)

# 카메라
st.markdown('<div class="section-card"><div class="section-header">📷 카메라 스캔</div>', unsafe_allow_html=True)
camera_photo = st.camera_input("카메라로 찍기", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 업로드
st.markdown('<div class="section-card"><div class="section-header">🖼️ 사진 업로드</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("JPG · PNG 이미지 업로드", type=["jpg","jpeg","png"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

image = None
image_bytes = None
if camera_photo:
    image = Image.open(camera_photo)
    image_bytes = camera_photo.getvalue()
elif uploaded_file:
    image = Image.open(uploaded_file)
    image_bytes = uploaded_file.getvalue()

if image:
    st.markdown('<div style="margin:0 1rem;">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 분석 버튼
st.markdown('<div class="analyze-wrap">', unsafe_allow_html=True)
analyze = st.button("🔍 신선도 분석하기", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 분석 결과
if analyze:
    if not image:
        st.warning("사진을 먼저 업로드하거나 촬영해주세요!")
    else:
        with st.spinner("AI가 분석 중이에요..."):
            image_data = base64.b64encode(image_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                        {"type": "text", "text": "이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:\n\n농산물 종류:\n신선도 점수: (숫자/10)\n상태: (신선/보통/주의/부패 중 하나)\n상태 설명:\n보관 방법:\n예상 남은 기한: "}
                    ]
                }]
            )
            result = response.choices[0].message.content
            lines = result.strip().split("\n")

            st.markdown('<div class="result-section"><div class="section-header">📊 분석 결과</div>', unsafe_allow_html=True)
            for line in lines:
                if not line.strip():
                    continue
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

# 가이드
guides = [
    ("🍎 사과", ["껍질 팽팽·광택 있음", "꼭지 싱싱·단단", "달콤한 향"], ["물렁·주름진 것", "검은 반점·곰팡이"]),
    ("🥦 브로콜리", ["짙은 초록색", "꽃봉오리 촘촘히 닫힘", "줄기 단단"], ["노란색 변색", "꽃이 핀 것"]),
    ("🍅 토마토", ["선명한 빨간색", "눌렀을 때 약간 탄력", "꼭지 초록 생기"], ["너무 물렁한 것", "갈라지거나 터진 것"]),
    ("🥕 당근", ["선명한 주황색", "표면 매끄럽고 단단", "잎이 선명한 녹색"], ["갈라지거나 물렁", "흰 줄기 많은 것"]),
    ("🍋 레몬", ["밝고 선명한 노란색", "묵직하고 단단", "향이 진함"], ["초록빛 남아있고 딱딱", "주름 많고 말라있는 것"]),
    ("🫐 블루베리", ["진한 보라-파란색", "흰 분같은 가루 있음", "단단하고 통통함"], ["빨간색 남아있는 것", "물컹하거나 즙 나오는 것"]),
]

st.markdown('<div class="guide-section"><div class="guide-title-bar">📗 농작물 고르는 가이드</div>', unsafe_allow_html=True)
for name, good, bad in guides:
    with st.expander(name):
        st.markdown(f'<div class="good">✔ 좋은 것<br>' + " · ".join(good) + '</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bad">✘ 피할 것<br>' + " · ".join(bad) + '</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer-bar">🌱 신선한 농산물로 건강한 하루!</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # phone-wrap
