import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; box-sizing: border-box; margin:0; padding:0; }
body, .main, .block-container { background: #e8f0e8 !important; padding: 0 !important; }
#MainMenu, header, footer { visibility: hidden; }
.block-container { max-width: 420px !important; margin: 0 auto !important; padding: 0 !important; }

/* 상태바 */
.status-bar {
    background: #1a1a1a;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 1.2rem;
    font-size: 0.78rem;
    font-weight: 700;
    border-radius: 30px 30px 0 0;
}

/* 초록 헤더 */
.app-header {
    background: linear-gradient(160deg, #4a7c3f 0%, #6aab5e 60%, #8dc87f 100%);
    padding: 1.2rem 1.3rem 1.5rem 1.3rem;
    color: white;
    position: relative;
}
.app-header-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 44px; height: 44px;
    background: rgba(255,255,255,0.25);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.app-title { font-size: 1.7rem; font-weight: 800; margin-bottom: 0.5rem; }
.app-sub1 { font-size: 0.9rem; font-weight: 400; opacity: 0.9; }
.app-sub2 { font-size: 1.1rem; font-weight: 700; }

/* 메인 바디 */
.app-body {
    background: #f2f7f0;
    padding: 1.2rem 1rem;
    border-radius: 0 0 30px 30px;
}

/* 섹션 라벨 */
.sec-label {
    font-size: 0.88rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* 카메라 카드 */
.camera-card {
    background: #1a2540;
    border-radius: 18px;
    padding: 2rem 1rem;
    text-align: center;
    color: white;
    position: relative;
    margin-bottom: 1.2rem;
}
.camera-corners::before, .camera-corners::after {
    content: '';
    position: absolute;
    width: 22px; height: 22px;
    border-color: #7dcc6a;
    border-style: solid;
}
.corner-tl { top: 10px; left: 10px; border-width: 3px 0 0 3px; border-radius: 4px 0 0 0; position:absolute; }
.corner-tr { top: 10px; right: 10px; border-width: 3px 3px 0 0; border-color: #7dcc6a; border-style:solid; border-radius: 0 4px 0 0; position:absolute; width:22px; height:22px; }
.corner-bl { bottom: 10px; left: 10px; border-width: 0 0 3px 3px; border-color: #7dcc6a; border-style:solid; border-radius: 0 0 0 4px; position:absolute; width:22px; height:22px; }
.corner-br { bottom: 10px; right: 10px; border-width: 0 3px 3px 0; border-color: #7dcc6a; border-style:solid; border-radius: 0 0 4px 0; position:absolute; width:22px; height:22px; }
.camera-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.camera-text { font-size: 1rem; font-weight: 700; margin-bottom: 0.2rem; }
.camera-sub { font-size: 0.78rem; opacity: 0.6; }

/* 업로드 카드 */
.upload-card {
    background: white;
    border: 2px dashed #aad4a0;
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 1.2rem;
}
.upload-icon-box {
    background: #fff8e1;
    border-radius: 12px;
    width: 48px; height: 48px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.upload-text-title { font-weight: 700; font-size: 0.95rem; color: #222; }
.upload-text-sub { font-size: 0.78rem; color: #aaa; }
.upload-arrow { margin-left: auto; color: #ccc; font-size: 1rem; }

/* 분석 버튼 */
.stButton > button {
    background: #2d5a27 !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    padding: 0.8rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    margin-bottom: 1rem;
}

/* 가이드 그리드 */
.guide-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.7rem;
    margin-top: 0.6rem;
}
.guide-item {
    background: white;
    border-radius: 16px;
    padding: 1rem 0.8rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.guide-emoji { font-size: 2rem; margin-bottom: 0.3rem; }
.guide-name { font-weight: 700; font-size: 0.92rem; color: #222; }
.guide-tap { font-size: 0.75rem; color: #aaa; }

.result-box {
    background: white;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)

# 상태바
st.markdown("""
<div class="status-bar">
  <span>9:41</span>
  <span>●●● WiFi 🔋</span>
</div>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="app-header">
  <div class="app-icon" style="position:absolute;top:1rem;right:1rem;width:44px;height:44px;background:rgba(255,255,255,0.25);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🌿</div>
  <div class="app-title">Scan Eat!</div>
  <div class="app-sub1">안녕하세요 👋</div>
  <div class="app-sub2">오늘의 신선도를 확인해볼까요?</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="app-body">', unsafe_allow_html=True)

# 카메라
st.markdown('<div class="sec-label">📷 카메라 스캔</div>', unsafe_allow_html=True)
st.markdown("""
<div class="camera-card">
  <div class="corner-tl"></div><div class="corner-tr"></div>
  <div class="corner-bl"></div><div class="corner-br"></div>
  <div class="camera-icon">📸</div>
  <div class="camera-text">카메라로 스캔하기</div>
  <div class="camera-sub">탭하여 카메라 시작</div>
</div>
""", unsafe_allow_html=True)
camera_photo = st.camera_input("카메라", label_visibility="collapsed")

# 업로드
st.markdown('<div class="sec-label">🖼️ 사진 업로드</div>', unsafe_allow_html=True)
st.markdown("""
<div class="upload-card">
  <div class="upload-icon-box">📁</div>
  <div>
    <div class="upload-text-title">갤러리에서 선택</div>
    <div class="upload-text-sub">JPG · PNG 이미지 업로드</div>
  </div>
  <div class="upload-arrow">›</div>
</div>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("업로드", type=["jpg","jpeg","png"], label_visibility="collapsed")

image = None
image_bytes = None
if camera_photo:
    image = Image.open(camera_photo)
    image_bytes = camera_photo.getvalue()
elif uploaded_file:
    image = Image.open(uploaded_file)
    image_bytes = uploaded_file.getvalue()

if image:
    st.image(image, use_container_width=True)

analyze = st.button("🔍 신선도 분석하기", use_container_width=True)

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
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("**📊 분석 결과**")
            for line in lines:
                if not line.strip(): continue
                if "농산물 종류" in line:
                    st.markdown(f"🥬 **{line.strip()}**")
                elif "신선도 점수" in line:
                    st.markdown(f"⭐ **{line.strip()}**")
                elif "상태:" in line:
                    val = line.split(":")[-1].strip()
                    if "신선" in val: st.success(f"📊 {line.strip()}")
                    elif "보통" in val: st.warning(f"📊 {line.strip()}")
                    else: st.error(f"📊 {line.strip()}")
                elif "상태 설명" in line:
                    st.info(f"💡 {line.strip()}")
                elif "보관 방법" in line:
                    st.markdown(f"🏪 {line.strip()}")
                elif "예상 남은 기한" in line:
                    st.markdown(f"⏰ {line.strip()}")
            st.markdown('</div>', unsafe_allow_html=True)

# 가이드
st.markdown('<div class="sec-label" style="margin-top:0.5rem;">📗 농작물 고르는 가이드</div>', unsafe_allow_html=True)

guides = [
    ("🍎", "사과", ["껍질 팽팽·광택 있음","꼭지 싱싱·단단","달콤한 향"], ["물렁·주름진 것","검은 반점·곰팡이"]),
    ("🥦", "브로콜리", ["짙은 초록색","꽃봉오리 촘촘히 닫힘","줄기 단단"], ["노란색 변색","꽃이 핀 것"]),
    ("🍅", "토마토", ["선명한 빨간색","눌렀을 때 약간 탄력","꼭지 초록 생기"], ["너무 물렁한 것","갈라지거나 터진 것"]),
    ("🥕", "당근", ["선명한 주황색","표면 매끄럽고 단단","잎이 선명한 녹색"], ["갈라지거나 물렁","흰 줄기 많은 것"]),
    ("🍋", "레몬", ["밝고 선명한 노란색","묵직하고 단단","향이 진함"], ["초록빛 남아있고 딱딱","주름 많고 말라있는 것"]),
    ("🫐", "블루베리", ["진한 보라-파란색","흰 분같은 가루 있음","단단하고 통통함"], ["빨간색 남아있는 것","물컹하거나 즙 나오는 것"]),
]

grid_html = '<div class="guide-grid">'
for emoji, name, good, bad in guides:
    grid_html += f"""
    <div class="guide-item">
      <div class="guide-emoji">{emoji}</div>
      <div class="guide-name">{name}</div>
      <div class="guide-tap">탭해서 보기</div>
    </div>"""
grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)

for emoji, name, good, bad in guides:
    with st.expander(f"{emoji} {name} 상세보기"):
        st.markdown(f'<span style="color:#2e7d32;font-weight:bold;">✔ 좋은 것</span><br><span style="color:#2e7d32;font-size:0.88rem;">' + " · ".join(good) + '</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color:#e53935;font-weight:bold;">✘ 피할 것</span><br><span style="color:#e53935;font-size:0.88rem;">' + " · ".join(bad) + '</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
