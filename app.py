import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def main():
    st.title("수학 문제 해결기")
    st.write("수학 문제를 입력하거나 이미지를 업로드한 후 문제를 입력하면 GPT가 해결해 드립니다.")

    # 이미지 업로드
    uploaded_file = st.file_uploader("수학 문제가 있는 이미지를 업로드하세요 (선택사항).", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

    # 사용자 입력
    user_input = st.text_area("여기에 수학 문제를 입력하세요:")

    if st.button("문제 해결"):
        if user_input:
            with st.spinner("문제를 해결 중입니다..."):
                solution = solve_math_problem(user_input)
            st.write("해답:")
            st.write(solution)
        else:
            st.warning("문제를 입력해 주세요.")

if __name__ == "__main__":
    main()
