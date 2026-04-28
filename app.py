import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Scan Eat!", page_icon="🌿", layout="centered")

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False
if "show_upload" not in st.session_state:
    st.session_state.show_upload = False
if "selected_guide" not in st.session_state:
    st.session_state.selected_guide = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; box-sizing: border-box; }
body, .main, .block-container { background: #e8ede8 !important; padding: 0 !important; }
#MainMenu, header, footer { visibility: hidden; }
.block-container { max-width: 420px !important; margin: 0 auto !important; padding: 0 0 2rem 0 !important; }

.status-bar {
    background: #1a1a1a; color: white;
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.4rem 1.2rem; font-size: 0.78rem; font-weight: 700;
}
.app-header {
    background: linear-gradient(160deg, #4a7c3f 0%, #6aab5e 60%, #8dc87f 100%);
    padding: 1.2rem 1.3rem 1.5rem 1.3rem; color: white; position: relative;
}
.header-icon {
    position: absolute; top: 1rem; right: 1rem;
    width: 44px; height: 44px;
    background: rgba(255,255,255,0.25); border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
}
.app-title { font-size: 1.7rem; font-weight: 800; margin-bottom: 0.4rem; }
.app-sub1 { font-size: 0.9rem; opacity: 0.9; }
.app-sub2 { font-size: 1.1rem; font-weight: 700; }

.app-body { background: #f2f7f0; padding: 1rem; }
.sec-label {
    font-size: 0.85rem; font-weight: 700; color: #555;
    margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.3rem;
}

/* 카메라/업로드 클릭 버튼 */
div[data-testid="stButton"] > button.camera-btn {
    background: #1a2540 !important; color: white !important;
    border-radius: 18px !important; border: none !important;
    padding: 2rem 1rem !important; width: 100% !important;
    font-size: 1rem !important; font-weight: 700 !important;
    margin-bottom: 0.4rem !important;
}

.camera-card-html {
    background: #1a2540; border-radius: 18px;
    padding: 1.8rem 1rem; text-align: center; color: white;
    margin-bottom: 0.3rem; cursor: pointer; position: relative;
}
.corner { position: absolute; width: 22px; height: 22px; border-color: #7dcc6a; border-style: solid; }
.tl { top:10px; left:10px; border-width: 3px 0 0 3px; border-radius: 4px 0 0 0; }
.tr { top:10px; right:10px; border-width: 3px 3px 0 0; border-radius: 0 4px 0 0; }
.bl { bottom:10px; left:10px; border-width: 0 0 3px 3px; border-radius: 0 0 0 4px; }
.br { bottom:10px; right:10px; border-width: 0 3px 3px 0; border-radius: 0 0 4px 0; }
.cam-icon { font-size: 2.2rem; margin-bottom: 0.4rem; }
.cam-title { font-weight: 700; font-size: 1rem; }
.cam-sub { font-size: 0.78rem; opacity: 0.6; }

.upload-card-html {
    background: white; border: 2px dashed #aad4a0; border-radius: 16px;
    padding: 0.9rem 1rem; display: flex; align-items: center; gap: 0.9rem;
    margin-bottom: 0.3rem;
}
.upload-icon { background: #fff8e1; border-radius: 12px; width:46px; height:46px;
    display:flex; align-items:center; justify-content:center; font-size:1.4rem; flex-shrink:0; }
.upload-title { font-weight: 700; font-size: 0.95rem; color: #222; }
.upload-sub { font-size: 0.78rem; color: #aaa; }
.upload-arr { margin-left: auto; color: #ccc; font-size: 1.1rem; }

/* 분석 버튼 */
.stButton > button {
    background: #2d5a27 !important; color: white !important;
    border-radius: 14px !important; border: none !important;
    padding: 0.8rem !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important;
}

/* 가이드 그리드 버튼 */
.guide-btn > button {
    background: white !important; color: #222 !important;
    border: 1px solid #e8e8e8 !important; border-radius: 16px !important;
    padding: 1rem 0.5rem !important; width: 100% !important;
    font-size: 0.88rem !important; font-weight: 700 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    min-height: 110px !important;
}
.guide-btn > button:hover { background: #f0f7ee !important; }

.guide-detail {
    background: white; border-radius: 14px;
    padding: 1rem 1.2rem; margin: 0.3rem 0 0.8rem 0;
    border-left: 4px solid #4a7c3f;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
}
.good-t { color: #2e7d32; font-weight: 700; font-size: 0.88rem; }
.bad-t { color: #e53935; font-weight: 700; font-size: 0.88rem; margin-top: 0.5rem; }
.result-box { background: white; border-radius: 16px; padding: 1rem 1.2rem;
    margin-bottom: 1rem; box-shadow: 0 1px 6px rgba(0,0,0,0.07); }
</style>
""", unsafe_allow_html=True)

# 상태바
st.markdown('<div class="status-bar"><span>9:41</span><span>●●● WiFi 🔋</span></div>', unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="app-header">
  <div class="header-icon">🌿</div>
  <div class="app-title">Scan Eat!</div>
  <div class="app-sub1">안녕하세요 👋</div>
  <div class="app-sub2">오늘의 신선도를 확인해볼까요?</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="app-body">', unsafe_allow_html=True)

# 카메라 카드 (클릭하면 카메라 열림)
st.markdown('<div class="sec-label">📷 카메라 스캔</div>', unsafe_allow_html=True)
st.markdown("""
<div class="camera-card-html">
  <div class="corner tl"></div><div class="corner tr"></div>
  <div class="corner bl"></div><div class="corner br"></div>
  <div class="cam-icon">📸</div>
  <div class="cam-title">카메라로 스캔하기</div>
  <div class="cam-sub">탭하여 카메라 시작</div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📷 카메라 열기", use_container_width=True):
        st.session_state.show_camera = not st.session_state.show_camera
        st.session_state.show_upload = False
with col2:
    if st.button("✕ 취소", use_container_width=True):
        st.session_state.show_camera = False

camera_photo = None
if st.session_state.show_camera:
    camera_photo = st.camera_input("📸 촬영", label_visibility="visible")

# 업로드 카드
st.markdown('<div class="sec-label" style="margin-top:0.8rem;">🖼️ 사진 업로드</div>', unsafe_allow_html=True)
st.markdown("""
<div class="upload-card-html">
  <div class="upload-icon">📁</div>
  <div>
    <div class="upload-title">갤러리에서 선택</div>
    <div class="upload-sub">JPG · PNG 이미지 업로드</div>
  </div>
  <div class="upload-arr">›</div>
</div>""", unsafe_allow_html=True)

if st.button("🖼️ 갤러리 열기", use_container_width=True):
    st.session_state.show_upload = not st.session_state.show_upload
    st.session_state.show_camera = False

uploaded_file = None
if st.session_state.show_upload:
    uploaded_file = st.file_uploader("이미지 선택", type=["jpg","jpeg","png"], label_visibility="collapsed")

image = None
image_bytes = None
if camera_photo:
    image = Image.open(camera_photo); image_bytes = camera_photo.getvalue()
elif uploaded_file:
    image = Image.open(uploaded_file); image_bytes = uploaded_file.getvalue()

if image:
    st.image(image, use_container_width=True)

# 분석 버튼
analyze = st.button("🔍 신선도 분석하기", use_container_width=True)

if analyze:
    if not image:
        st.warning("사진을 먼저 업로드하거나 촬영해주세요!")
    else:
        with st.spinner("AI가 분석 중이에요..."):
            image_data = base64.b64encode(image_bytes).decode("utf-8")
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                    {"type": "text", "text": "이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:\n\n농산물 종류:\n신선도 점수: (숫자/10)\n상태: (신선/보통/주의/부패 중 하나)\n상태 설명:\n보관 방법:\n예상 남은 기한: "}
                ]}]
            )
            result = response.choices[0].message.content
            lines = result.strip().split("\n")
            st.markdown('<div class="result-box"><strong>📊 분석 결과</strong><br>', unsafe_allow_html=True)
            for line in lines:
                if not line.strip(): continue
                if "농산물 종류" in line: st.markdown(f"🥬 **{line.strip()}**")
                elif "신선도 점수" in line: st.markdown(f"⭐ **{line.strip()}**")
                elif "상태:" in line:
                    val = line.split(":")[-1].strip()
                    if "신선" in val: st.success(f"📊 {line.strip()}")
                    elif "보통" in val: st.warning(f"📊 {line.strip()}")
                    else: st.error(f"📊 {line.strip()}")
                elif "상태 설명" in line: st.info(f"💡 {line.strip()}")
                elif "보관 방법" in line: st.markdown(f"🏪 {line.strip()}")
                elif "예상 남은 기한" in line: st.markdown(f"⏰ {line.strip()}")
            st.markdown('</div>', unsafe_allow_html=True)

# 가이드 그리드
st.markdown('<div class="sec-label" style="margin-top:1rem;">📗 농작물 고르는 가이드</div>', unsafe_allow_html=True)

guides = [
    ("🍎", "사과", ["껍질 팽팽·광택 있음","꼭지 싱싱·단단","달콤한 향"], ["물렁·주름진 것","검은 반점·곰팡이"]),
    ("🥦", "브로콜리", ["짙은 초록색","꽃봉오리 촘촘히 닫힘","줄기 단단"], ["노란색 변색","꽃이 핀 것"]),
    ("🍅", "토마토", ["선명한 빨간색","눌렀을 때 약간 탄력","꼭지 초록 생기"], ["너무 물렁한 것","갈라지거나 터진 것"]),
    ("🥕", "당근", ["선명한 주황색","표면 매끄럽고 단단","잎이 선명한 녹색"], ["갈라지거나 물렁","흰 줄기 많은 것"]),
    ("🍋", "레몬", ["밝고 선명한 노란색","묵직하고 단단","향이 진함"], ["초록빛 남아있고 딱딱","주름 많고 말라있는 것"]),
    ("🫐", "블루베리", ["진한 보라-파란색","흰 분같은 가루 있음","단단하고 통통함"], ["빨간색 남아있는 것","물컹하거나 즙 나오는 것"]),
]

# 2열 그리드로 버튼 배치
for i in range(0, len(guides), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(guides):
            emoji, name, good, bad = guides[idx]
            with col:
                st.markdown(f'<div class="guide-btn">', unsafe_allow_html=True)
                if st.button(f"{emoji}\n{name}\n탭해서 보기", key=f"guide_{idx}", use_container_width=True):
                    if st.session_state.selected_guide == idx:
                        st.session_state.selected_guide = None
                    else:
                        st.session_state.selected_guide = idx
                st.markdown('</div>', unsafe_allow_html=True)

    # 이 행에 선택된 항목 있으면 상세 바로 아래 표시
    for j in range(2):
        idx = i + j
        if idx < len(guides) and st.session_state.selected_guide == idx:
            emoji, name, good, bad = guides[idx]
            st.markdown(f"""
            <div class="guide-detail">
              <div style="font-weight:800;font-size:1rem;margin-bottom:0.6rem;">{emoji} {name}</div>
              <div class="good-t">✔ 좋은 것</div>
              <div style="color:#388e3c;font-size:0.85rem;margin-bottom:0.5rem;">{"  ·  ".join(good)}</div>
              <div class="bad-t">✘ 피할 것</div>
              <div style="color:#e53935;font-size:0.85rem;">{"  ·  ".join(bad)}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center;color:#bbb;font-size:0.75rem;margin-top:1.5rem;">🌱 신선한 농산물로 건강한 하루!</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
