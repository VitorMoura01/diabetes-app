import streamlit as st
import os
import base64

# From: https://discuss.streamlit.io/t/href-on-image/9693/3
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache_data()
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace(".", "")
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f"""
        <a href="{target_url}">
            <img class="screenshot" src="data:image/{img_format};base64,{bin_str}" style="max-width: 100%;"/>
        </a>"""
    return html_code


def linked_image(image, target_url):
    """Shows an image with a link."""
    st.write(get_img_with_href(image, target_url), unsafe_allow_html=True)