import streamlit as st
import google.genai as genai
from PIL import Image
import textwrap
import base64

# Configure client
client = genai.Client(api_key='')

# Model name
model_name = 'models/gemini-2.5-flash'

st.title("Gemini AI App")

# Text generation section
st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Generate Response"):
    if question:
        response = client.models.generate_content(model=model_name, contents=question)
        st.markdown("**Response:**")
        st.markdown(textwrap.indent(response.candidates[0].content.parts[0].text, '> '))
    else:
        st.warning("Please enter a question.")

# Image description section
st.header("Describe an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    if st.button("Generate Description"):
        # Encode image to base64
        uploaded_file.seek(0)
        image_data = base64.b64encode(uploaded_file.read()).decode('utf-8')
        mime_type = uploaded_file.type
        contents = [
            {'text': 'Generate Description'},
            {'inline_data': {'mime_type': mime_type, 'data': image_data}}
        ]
        response = client.models.generate_content(model=model_name, contents=contents)
        st.markdown("**Description:**")
        st.markdown(textwrap.indent(response.candidates[0].content.parts[0].text, '> '))

# Topic selection
st.header("Learn About a Topic")
topic = st.selectbox("Choose a topic:", ["Select", "A: Space", "B: Oceans"])
if topic == "A: Space":
    sub_q = 'Space'
elif topic == "B: Oceans":
    sub_q = 'tell me about deep ocean science fact'
else:
    sub_q = None

if sub_q and st.button("Get Information"):
    response = client.models.generate_content(model=model_name, contents=sub_q)
    st.markdown(f"**Asking Gemini about {sub_q}:**")
    st.markdown(textwrap.indent(response.candidates[0].content.parts[0].text, '> '))
