import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import io

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tesseract OCR 설정 (Windows 사용자의 경우)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def solve_math_problem(problem):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that solves math problems."},
                {"role": "user", "content": f"Please solve this math problem: {problem}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"이미지에서 텍스트를 추출하는 중 오류가 발생했습니다: {str(e)}"

def main():
    st.title("수학 문제 해결기")
    st.write("수학 문제를 입력하거나 이미지를 업로드하면 GPT가 해결해 드립니다.")

    # 사용자 입력 방식 선택
    input_method = st.radio("입력 방식을 선택하세요:", ("텍스트 입력", "이미지 업로드"))

    if input_method == "텍스트 입력":
        user_input = st.text_area("여기에 수학 문제를 입력하세요:")
    else:
        uploaded_file = st.file_uploader("수학 문제가 있는 이미지를 업로드하세요.", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)
            user_input = extract_text_from_image(image)
            st.write("추출된 텍스트:")
            st.write(user_input)

    if st.button("문제 해결"):
        if user_input:
            with st.spinner("문제를 해결 중입니다..."):
                solution = solve_math_problem(user_input)
            st.write("해답:")
            st.write(solution)
        else:
            st.warning("문제를 입력하거나 이미지를 업로드해 주세요.")

if __name__ == "__main__":
    main()
