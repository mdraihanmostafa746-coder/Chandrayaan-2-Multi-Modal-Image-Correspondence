import streamlit as st

st.set_page_config(
    page_title="Chandrayaan-2 Image Correspondence",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ Chandrayaan-2 Multi-Modal Image Correspondence")
st.write(
    "Upload satellite images and compare their visual correspondence "
    "using image processing and feature matching."
)

st.sidebar.header("Navigation")

page = st.sidebar.selectbox(
    "Choose a section",
    [
        "Home",
        "Image Upload",
        "Feature Matching",
        "Results"
    ]
)

if page == "Home":
    st.subheader("Project Overview")
    st.info(
        "This application will compare Chandrayaan-2 satellite images "
        "using preprocessing, feature matching and RANSAC verification."
    )

elif page == "Image Upload":
    st.subheader("Upload Satellite Images")

    image_1 = st.file_uploader(
        "Upload First Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    image_2 = st.file_uploader(
        "Upload Second Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if image_1 and image_2:
        col1, col2 = st.columns(2)

        with col1:
            st.image(image_1, caption="First Image", use_container_width=True)

        with col2:
            st.image(image_2, caption="Second Image", use_container_width=True)

elif page == "Feature Matching":
    st.subheader("Feature Matching")
    st.warning("Feature matching module will be connected here.")

elif page == "Results":
    st.subheader("Matching Results")
    st.warning("Final matching results will be displayed here.")