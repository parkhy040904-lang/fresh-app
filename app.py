import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key=“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”)

st.set_page_config(page_title=“Scan Eat!”, page_icon=“🌿”, layout=“centered”)

if “show_camera” not in st.session_state:
st.session_state.show_camera = False
if “show_upload” not in st.session_state:
st.session_state.show_upload = False
if “selected_guide” not in st.session_state:
st.session_state.selected_guide = None

st.markdown(”””

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

/* 카메라 박스 버튼 - 연두색 */
.camera-btn-wrap .stButton > button {
    background: #a8e063 !important; color: #1a2540 !important;
    border-radius: 18px !important; border: none !important;
    padding: 2rem 1rem !important; width: 100% !important;
    font-size: 1rem !important; font-weight: 700 !important;
    min-height: 110px !important; box-shadow: none !important;
    white-space: pre-line !important; line-height: 2 !important;
    outline: 2px solid #6fcf3a !important; outline-offset: -10px !important;
}
.camera-btn-wrap .stButton > button:hover { background: #95d94e !important; }

/* 업로드 박스 버튼 - 연두색 */
.upload-btn-wrap .stButton > button {
    background: #a8e063 !important; color: #1a2540 !important;
    border: 2px dashed #6fcf3a !important; border-radius: 16px !important;
    padding: 0.9rem 1rem !important; width: 100% !important;
    font-size: 0.95rem !important; font-weight: 700 !important;
    min-height: unset !important; box-shadow: none !important;
    white-space: pre-line !important; line-height: 1.8 !important;
}
.upload-btn-wrap .stButton > button:hover { background: #95d94e !important; }

/* 분석 버튼 */
.analyze-btn-wrap .stButton > button {
    background: #2d5a27 !important; color: white !important;
    border-radius: 14px !important; border: none !important;
    padding: 0.8rem !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important;
    min-height: unset !important; box-shadow: none !important;
}

/* 가이드 버튼 - 흰색 */
.stButton > button {
    background: white !important; color: #222 !important;
    border: 1px solid #e8e8e8 !important; border-radius: 16px !important;
    padding: 1rem 0.5rem !important; font-size: 0.88rem !important;
    font-weight: 700 !important; width: 100% !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    min-height: 80px !important;
}
.stButton > button:hover { background: #f0f7ee !important; }

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

“””, unsafe_allow_html=True)

# 상태바

st.markdown(’<div class="status-bar"><span>9:41</span><span>●●● WiFi 🔋</span></div>’, unsafe_allow_html=True)

# 헤더

st.markdown(”””

<div class="app-header">
  <div class="header-icon">🌿</div>
  <div class="app-title">Scan Eat!</div>
  <div class="app-sub1">안녕하세요 👋</div>
  <div class="app-sub2">오늘의 신선도를 확인해볼까요?</div>
</div>
""", unsafe_allow_html=True)

st.markdown(’<div class="app-body">’, unsafe_allow_html=True)

# 카메라 카드

st.markdown(’<div class="sec-label">📷 카메라 스캔</div>’, unsafe_allow_html=True)
st.markdown(’<div class="camera-btn-wrap">’, unsafe_allow_html=True)
if st.button(“📸  카메라로 스캔하기”, key=“cam_btn”, use_container_width=True):
st.session_state.show_camera = not st.session_state.show_camera
st.session_state.show_upload = False
st.markdown(’</div>’, unsafe_allow_html=True)

camera_photo = None
if st.session_state.show_camera:
camera_photo = st.camera_input(“📸 촬영”, label_visibility=“visible”)

# 업로드 카드

st.markdown(’<div class="sec-label" style="margin-top:0.8rem;">🖼️ 사진 업로드</div>’, unsafe_allow_html=True)
st.markdown(’<div class="upload-btn-wrap">’, unsafe_allow_html=True)
if st.button(“📁  갤러리에서 선택”, key=“upload_btn”, use_container_width=True):
st.session_state.show_upload = not st.session_state.show_upload
st.session_state.show_camera = False
st.markdown(’</div>’, unsafe_allow_html=True)

uploaded_file = None
if st.session_state.show_upload:
uploaded_file = st.file_uploader(“이미지 선택”, type=[“jpg”,“jpeg”,“png”], label_visibility=“collapsed”)

image = None
image_bytes = None
if camera_photo:
image = Image.open(camera_photo); image_bytes = camera_photo.getvalue()
elif uploaded_file:
image = Image.open(uploaded_file); image_bytes = uploaded_file.getvalue()

if image:
st.image(image, use_container_width=True)

# 분석 버튼

st.markdown(’<div class="analyze-btn-wrap">’, unsafe_allow_html=True)
analyze = st.button(“🔍 신선도 분석하기”, use_container_width=True)
st.markdown(’</div>’, unsafe_allow_html=True)

if analyze:
if not image:
st.warning(“사진을 먼저 업로드하거나 촬영해주세요!”)
else:
with st.spinner(“AI가 분석 중이에요…”):
image_data = base64.b64encode(image_bytes).decode(“utf-8”)
response = client.chat.completions.create(
model=“meta-llama/llama-4-scout-17b-16e-instruct”,
messages=[{“role”: “user”, “content”: [
{“type”: “image_url”, “image_url”: {“url”: f”data:image/jpeg;base64,{image_data}”}},
{“type”: “text”, “text”: “이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:\n\n농산물 종류:\n신선도 점수: (숫자/10)\n상태: (신선/보통/주의/부패 중 하나)\n상태 설명:\n보관 방법:\n예상 남은 기한: “}
]}]
)
result = response.choices[0].message.content
lines = result.strip().split(”\n”)
st.markdown(’<div class="result-box"><strong>📊 분석 결과</strong><br>’, unsafe_allow_html=True)
for line in lines:
if not line.strip(): continue
if “농산물 종류” in line: st.markdown(f”🥬 **{line.strip()}**”)
elif “신선도 점수” in line: st.markdown(f”⭐ **{line.strip()}**”)
elif “상태:” in line:
val = line.split(”:”)[-1].strip()
if “신선” in val: st.success(f”📊 {line.strip()}”)
elif “보통” in val: st.warning(f”📊 {line.strip()}”)
else: st.error(f”📊 {line.strip()}”)
elif “상태 설명” in line: st.info(f”💡 {line.strip()}”)
elif “보관 방법” in line: st.markdown(f”🏪 {line.strip()}”)
elif “예상 남은 기한” in line: st.markdown(f”⏰ {line.strip()}”)
st.markdown(’</div>’, unsafe_allow_html=True)

# 가이드 그리드

st.markdown(’<div class="sec-label" style="margin-top:1rem;">📗 농작물 고르는 가이드</div>’, unsafe_allow_html=True)

guides = [
(“🍉”, “수박”, [“두드렸을 때 탁한 소리”, “줄무늬 선명하고 윤기”, “배꼽 작고 건조”, “묵직한 무게”], [“두드렸을 때 맑은 소리”, “꼭지 없거나 시든 것”]),
(“🍎”, “사과”, [“껍질 팽팽·광택 있음”, “꼭지 싱싱·단단”, “달콤한 향”], [“물렁·주름진 것”, “검은 반점·곰팡이”]),
(“🍓”, “딸기”, [“전체 선명한 빨간색”, “꼭지 초록 싱싱”, “향 진하고 통통함”], [“흰 부분 남은 미숙한 것”, “물컹하거나 즙 새는 것”]),
(“🥬”, “배추”, [“잎 빳빳하고 선명한 초록”, “속 꽉 차고 묵직함”, “밑동 하얗고 단단”], [“잎 시들고 노란 것”, “속 비어 가벼운 것”]),
(“🧅”, “양파”, [“껍질 얇고 광택·건조”, “단단하고 묵직함”, “목 부분 건조”], [“싹이 난 것”, “물렁하거나 냄새 심한 것”]),
(“🍃”, “무”, [“묵직하고 단단함”, “껍질 매끄럽고 흰색”, “잎 초록 싱싱”], [“바람 들어 가벼운 것”, “갈라지거나 물렁한 것”]),
]

for i in range(0, len(guides), 2):
cols = st.columns(2)
for j, col in enumerate(cols):
idx = i + j
if idx < len(guides):
emoji, name, good, bad = guides[idx]
with col:
if st.button(f”{emoji}\n{name}”, key=f”guide_{idx}”, use_container_width=True):
if st.session_state.selected_guide == idx:
st.session_state.selected_guide = None
else:
st.session_state.selected_guide = idx

```
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
```

st.markdown(’<div style="text-align:center;color:#aaa;font-size:0.78rem;padding:1rem 0;">Scan Eat! © 2024</div>’, unsafe_allow_html=True)
st.markdown(’</div>’, unsafe_allow_html=True)