from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


# take environment variables from .env.
load_dotenv()


import google.generativeai as genai

os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))





# Configure api key 
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))


## LOad anf get response from gemini-pro-vision model

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text



#image setup 

def image_setup(image):
    if image is not None:

        # Read the file into bytes

        image_bytes = image.getvalue()

        # Get the media type of the image 

        image_parts = [
            {
                "mime_type": image.type,  
                "data": image_bytes
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No Image is uploaded")
    


st.set_page_config(page_title="Gemini Medicine App")

st.header("Medicine App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Description of Medicine")

input_prompt= """

Provide details of the medicine detected in the image using the following format:

### Medicine Details:
- **Name:** [Provide the name of the medicine]
- **Symptoms:** [List the symptoms the medicine is intended to treat]
- **Primary Diagnosis:** [Specify the primary medical condition or diagnosis]
- **Usage:** [Describe how the medicine is typically used]
- **Dosage:** [Specify the recommended dosage]
- **Description:**
  - [Include any additional information or description about the medicine]

### Safety and Side Effects:
- **Possible Side Effects:** [List potential side effects of the medicine]
- **Contraindications:** [Specify any conditions or situations where the medicine should not be used]
- **Warnings:** [Provide important warnings or precautions related to the medicine]

### Storage and Administration:
- **Storage Instructions:** [Specify how the medicine should be stored]
- **Administration Guidelines:** [Provide instructions on how to administer the medicine]

### Additional Information:
- **Manufacturer:** [Specify the manufacturer of the medicine]
- **Availability:** [Indicate if the medicine is prescription-only or available over-the-counter]
- **Cost:** [Provide information about the cost or pricing both in Dollars and INR]



"""
                

## If submit button is clicked

if submit:
    image_data=image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)