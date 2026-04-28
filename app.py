import streamlit as st
from PIL import Image
import base64
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="농산물 신선도 체커", page_icon="🥬", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8fff8; }
    .title { text-align: center; color: #2e7d32; font-size: 2.5rem; font-weight: bold; margin-bottom: 0; }
    .subtitle { text-align: center; color: #666; font-size: 1rem; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🥬 농산물 신선도 체커</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">사진을 올리면 AI가 신선도를 분석해드려요!</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📁 사진 업로드", "📷 카메라로 찍기"])

image = None
image_bytes = None

with tab1:
    uploaded_file = st.file_uploader("농산물 사진을 올려주세요", type=["jpg", "jpeg", "png"])
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

    if st.button("🔍 신선도 분석하기", use_container_width=True):
        with st.spinner("AI가 분석 중이에요..."):
            image_data = base64.b64encode(image_bytes).decode("utf-8")

            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        },
                        {
                            "type": "text",
                            "text": """이 농산물 사진을 보고 아래 항목을 분석해주세요. 반드시 아래 형식으로만 답하세요:

농산물 종류:
신선도 점수: (숫자/10)
상태: (신선/보통/주의/부패 중 하나)
상태 설명:
보관 방법:
예상 남은 기한: """
                        }
                    ]
                }]
            )

            result = response.choices[0].message.content
            lines = result.strip().split("\n")

            st.success("분석 완료!")
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

st.markdown("---")
st.markdown('<p style="text-align:center; color:#aaa; font-size:0.8rem;">🌱 신선한 농산물로 건강한 하루!</p>', unsafe_allow_html=True)
