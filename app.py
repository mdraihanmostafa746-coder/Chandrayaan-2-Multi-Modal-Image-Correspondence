import streamlit as st

st.set_page_config(
    page_title="Chandrayaan-2 Image Correspondence",
    page_icon="🛰️",
    layout="wide"
)

# ---------- Custom Styling ----------
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
        margin-bottom: 30px;
    }

    .section-card {
        background: #12243d;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #243b5a;
        margin-bottom: 20px;
    }

    .feature-card {
        background: #10213a;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #294361;
    }

    .feature-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
    }

    .feature-text {
        color: #aebed6;
        font-size: 14px;
    }

    .metric-card {
        background: #142a47;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #315174;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Sidebar ----------
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

# ---------- Home ----------
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
                <h3>🛡️ RANSAC</h3>
                <p class="feature-text">
                Remove incorrect matches and verify reliable points.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------- Image Upload ----------
elif page == "Image Upload":

    st.markdown(
        '<div class="main-title">Upload Satellite Images</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload two images for correspondence analysis.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First Image")
        image_1 = st.file_uploader(
            "Upload first satellite image",
            type=["png", "jpg", "jpeg", "webp"],
            key="image_1"
        )

        if image_1:
            st.image(
                image_1,
                caption="Image 1",
                use_container_width=True
            )

    with col2:
        st.subheader("Second Image")
        image_2 = st.file_uploader(
            "Upload second satellite image",
            type=["png", "jpg", "jpeg", "webp"],
            key="image_2"
        )

        if image_2:
            st.image(
                image_2,
                caption="Image 2",
                use_container_width=True
            )

    if image_1 and image_2:
        st.success("Both images uploaded successfully.")
        st.info("Now go to the Feature Matching section.")

# ---------- Feature Matching ----------
elif page == "Feature Matching":

    st.markdown(
        '<div class="main-title">Feature Matching</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Configure the matching process.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        detector = st.selectbox(
            "Feature Detector",
            ["ORB", "SIFT", "AKAZE"]
        )

    with col2:
        matcher = st.selectbox(
            "Matcher",
            ["BFMatcher", "FLANN"]
        )

    with col3:
        threshold = st.number_input(
            "RANSAC Threshold",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=1.0
        )

    st.markdown("---")

    if st.button("▶ Run Matching", use_container_width=True):
        st.success("Matching configuration selected.")
        st.write(f"Detector: **{detector}**")
        st.write(f"Matcher: **{matcher}**")
        st.write(f"RANSAC Threshold: **{threshold}**")
        st.info("Actual matching pipeline will be connected in the next step.")

# ---------- Results ----------
elif page == "Results":

    st.markdown(
        '<div class="main-title">Matching Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">View matching statistics and verification results.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card"><h3>0</h3><p>Keypoints 1</p></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card"><h3>0</h3><p>Keypoints 2</p></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card"><h3>0</h3><p>Good Matches</p></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card"><h3>0.000</h3><p>Matching Score</p></div>',
            unsafe_allow_html=True
        )

    st.info("Run the matching process to display actual results.")