import streamlit as st
from streamlit_image_comparison import image_comparison
from application import process_image,BEFORE_FOLDER_PATH,AFTER_FOLDER_PATH,map_models
from PIL import Image
st.title('Hawkeye')


st.write('Upload an image to see the difference between the original and the upscaled image')

models = map_models()
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    before_img_path = f'{BEFORE_FOLDER_PATH}/{uploaded_file.name}'
    after_img_path = f'{AFTER_FOLDER_PATH}/{uploaded_file.name}'
    with open(before_img_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    for model in models.keys():
        process_image(before_img_path,after_img_path,model)
        before_img = Image.open(before_img_path).resize((512,512),Image.Resampling.LANCZOS)
        after_img = Image.open(after_img_path).resize((512,512),Image.Resampling.LANCZOS)
        st.write(f'Upscaled Image using {model}')
        image_comparison(before_img, after_img,'Original','Upscaled')

    # st.image(img, caption='Uploaded Image.', width=512)
    # st.button('Process Image')
    # Normalize pixel values