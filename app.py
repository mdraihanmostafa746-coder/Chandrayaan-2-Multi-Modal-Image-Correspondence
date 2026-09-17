import streamlit as st

from src.ui_matching import run_orb_matching


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Chandrayaan-2 Image Correspondence",
    page_icon="🛰️",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #071426, #0d1d35);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: #081525;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #aebed6;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .section-card {
        background: #12243d;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #294361;
        margin-bottom: 20px;
    }

    .feature-card {
        background: #10213a;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #294361;
    }

    .feature-title {
        color: white;
        font-size: 19px;
        font-weight: 600;
    }

    .feature-text {
        color: #aebed6;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "image_1" not in st.session_state:
    st.session_state.image_1 = None

if "image_2" not in st.session_state:
    st.session_state.image_2 = None

if "matching_result" not in st.session_state:
    st.session_state.matching_result = None


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("🛰️ Chandrayaan-2")
st.sidebar.caption("Image Correspondence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Image Upload",
        "Feature Matching",
        "Results"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Better Images")
st.sidebar.caption("Better Insights")
st.sidebar.caption("From Space")


# --------------------------------------------------
# Home Page
# --------------------------------------------------

if page == "Home":

    st.markdown(
        '<div class="main-title">Chandrayaan-2 Multi-Modal Image Correspondence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Compare satellite images using preprocessing, feature matching and RANSAC verification.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h2>Project Overview</h2>
            <p>
            This application compares Chandrayaan-2 satellite images
            from different sensors and identifies reliable visual correspondences.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🖼️ Preprocessing</h3>
                <p class="feature-text">
                Improve image quality and reduce noise.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🔍 Feature Matching</h3>
                <p class="feature-text">
                Detect and match important image features.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🛡️ RANSAC Verification</h3>
                <p class="feature-text">
                Verify reliable feature correspondences.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# Image Upload Page
# --------------------------------------------------

elif page == "Image Upload":

    st.markdown(
        '<div class="main-title">Upload Satellite Images</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload two satellite images for correspondence analysis.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("First Image")

        uploaded_image_1 = st.file_uploader(
            "Choose the first image",
            type=["png", "jpg", "jpeg", "webp"],
            key="uploaded_image_1"
        )

        if uploaded_image_1 is not None:
            st.session_state.image_1 = uploaded_image_1

    with col2:

        st.subheader("Second Image")

        uploaded_image_2 = st.file_uploader(
            "Choose the second image",
            type=["png", "jpg", "jpeg", "webp"],
            key="uploaded_image_2"
        )

        if uploaded_image_2 is not None:
            st.session_state.image_2 = uploaded_image_2

    st.markdown("---")

    preview_col1, preview_col2 = st.columns(2)

    with preview_col1:

        if st.session_state.image_1 is not None:
            st.image(
                st.session_state.image_1,
                caption="Image 1 Preview",
                use_container_width=True
            )
        else:
            st.info("No first image selected.")

    with preview_col2:

        if st.session_state.image_2 is not None:
            st.image(
                st.session_state.image_2,
                caption="Image 2 Preview",
                use_container_width=True
            )
        else:
            st.info("No second image selected.")

    if (
        st.session_state.image_1 is not None
        and st.session_state.image_2 is not None
    ):
        st.success("Both images are ready for feature matching.")
        st.info("Open the Feature Matching section from the sidebar.")


# --------------------------------------------------
# Feature Matching Page
# --------------------------------------------------

elif page == "Feature Matching":

    st.markdown(
        '<div class="main-title">Feature Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Run ORB feature matching with Gaussian Blur preprocessing.</div>',
        unsafe_allow_html=True
    )

    if (
        st.session_state.image_1 is None
        or st.session_state.image_2 is None
    ):

        st.warning(
            "Please upload both images from the Image Upload section first."
        )

    else:

        st.success("Both images are loaded successfully.")

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                st.session_state.image_1,
                caption="Image 1",
                use_container_width=True
            )

        with col2:
            st.image(
                st.session_state.image_2,
                caption="Image 2",
                use_container_width=True
            )

        st.markdown("---")

        st.subheader("Matching Configuration")

        detector = st.selectbox(
            "Feature Detector",
            ["ORB"],
            index=0
        )

        st.write("Preprocessing: Gaussian Blur")
        st.write("Matcher: BFMatcher with Hamming Distance")
        st.write("Ratio Test: 0.75")

        if st.button(
            "▶ Run ORB Matching",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner("Running ORB feature matching..."):

                    result = run_orb_matching(
                        st.session_state.image_1.getvalue(),
                        st.session_state.image_2.getvalue()
                    )

                    st.session_state.matching_result = result

                st.success("ORB matching completed successfully.")

            except Exception as error:

                st.error(f"Matching failed: {error}")

        result = st.session_state.matching_result

        if result is not None:

            st.markdown("---")
            st.subheader("Matching Results")

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric(
                    "Keypoints Image 1",
                    result["keypoints_1"]
                )

            with metric_col2:
                st.metric(
                    "Keypoints Image 2",
                    result["keypoints_2"]
                )

            with metric_col3:
                st.metric(
                    "Good Matches",
                    result["good_matches"]
                )

            with metric_col4:
                st.metric(
                    "Matching Score",
                    f'{result["matching_score"]:.4f}'
                )

            st.subheader("ORB Matched Keypoints")

            st.image(
                result["matched_image"],
                caption="ORB Feature Correspondences",
                use_container_width=True
            )


# --------------------------------------------------
# Results Page
# --------------------------------------------------

elif page == "Results":

    st.markdown(
        '<div class="main-title">Matching Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View the output of the image matching process.</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.matching_result

    if result is None:

        st.info(
            "No matching result available. Upload two images and run ORB Matching first."
        )

    else:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Keypoints Image 1",
                result["keypoints_1"]
            )

        with col2:
            st.metric(
                "Keypoints Image 2",
                result["keypoints_2"]
            )

        with col3:
            st.metric(
                "Good Matches",
                result["good_matches"]
            )

        with col4:
            st.metric(
                "Matching Score",
                f'{result["matching_score"]:.4f}'
            )

        st.subheader("Matched Keypoints Visualization")

        st.image(
            result["matched_image"],
            caption="ORB Feature Correspondences",
            use_container_width=True
        )