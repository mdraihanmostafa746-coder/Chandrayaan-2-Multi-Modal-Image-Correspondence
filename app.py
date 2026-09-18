import textwrap
import cv2
import numpy as np
import streamlit as st

from src.ui_matching import run_orb_matching


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Chandrayaan-2 | Image Correspondence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HELPER FOR CLEAN HTML RENDERING
# ============================================================


def render_html(content):
  st.markdown(textwrap.dedent(content), unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "image_1" not in st.session_state:
  st.session_state.image_1 = None

if "image_2" not in st.session_state:
  st.session_state.image_2 = None

if "image_1_name" not in st.session_state:
  st.session_state.image_1_name = None

if "image_2_name" not in st.session_state:
  st.session_state.image_2_name = None

if "matching_result" not in st.session_state:
  st.session_state.matching_result = None


# ============================================================
# PREMIUM CSS
# ============================================================

render_html("""
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(39, 112, 190, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 85%,
                rgba(25, 72, 125, 0.18),
                transparent 32%
            ),
            linear-gradient(
                135deg,
                #030914 0%,
                #07172b 45%,
                #081a2f 100%
            );
        color: #f8fafc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #030b17 0%,
                #061526 55%,
                #04101e 100%
            );
        border-right: 1px solid rgba(75, 145, 210, 0.30);
    }

    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    [data-testid="stSidebar"] p {
        color: #8ba4bf;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(90, 130, 170, 0.25);
    }

    .main-title {
        font-size: 43px;
        line-height: 1.08;
        font-weight: 850;
        letter-spacing: -1.5px;
        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #dceeff 45%,
                #63b6ff 100%
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }

    .subtitle {
        color: #91aac5;
        font-size: 16px;
        line-height: 1.7;
        max-width: 900px;
        margin-bottom: 28px;
    }

    .hero-card {
        position: relative;
        overflow: hidden;
        padding: 42px;
        border-radius: 24px;
        border: 1px solid rgba(75, 157, 230, 0.45);
        background:
            linear-gradient(
                115deg,
                rgba(18, 61, 103, 0.96),
                rgba(7, 25, 46, 0.95)
            );
        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 25px;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        width: 450px;
        height: 450px;
        right: -200px;
        top: -220px;
        border-radius: 50%;
        background:
            radial-gradient(
                circle,
                rgba(63, 157, 245, 0.20),
                transparent 65%
            );
    }

    .hero-card:after {
        content: "🛰️";
        position: absolute;
        right: 55px;
        top: 40px;
        font-size: 105px;
        opacity: 0.12;
    }

    .hero-label {
        color: #55b5ff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 13px;
    }

    .hero-heading {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.6px;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #b8cce2;
        font-size: 16px;
        line-height: 1.75;
        max-width: 760px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 15px;
        border-radius: 50px;
        background: rgba(27, 203, 143, 0.10);
        border: 1px solid rgba(50, 220, 160, 0.35);
        color: #63e7b5;
        font-size: 13px;
        font-weight: 700;
    }

    .section-card {
        background:
            linear-gradient(
                145deg,
                rgba(18, 43, 72, 0.94),
                rgba(9, 27, 48, 0.94)
            );
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(69, 115, 157, 0.40);
        box-shadow: 0 12px 35px rgba(0,0,0,0.20);
        margin-bottom: 23px;
    }

    .section-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .section-description {
        color: #a9bfd7;
        line-height: 1.7;
        font-size: 15px;
    }

    .feature-card {
        position: relative;
        min-height: 205px;
        padding: 28px;
        border-radius: 20px;
        background:
            linear-gradient(
                145deg,
                rgba(17, 43, 72, 0.95),
                rgba(8, 25, 44, 0.96)
            );
        border: 1px solid rgba(68, 113, 155, 0.42);
        box-shadow: 0 14px 35px rgba(0,0,0,0.20);
    }

    .feature-icon {
        font-size: 34px;
        margin-bottom: 15px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .feature-text {
        color: #9fb6cf;
        font-size: 14px;
        line-height: 1.65;
    }

    .workflow-card {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 18px 20px;
        border-radius: 15px;
        background: rgba(12, 34, 59, 0.80);
        border: 1px solid rgba(65, 108, 149, 0.35);
    }

    .workflow-number {
        min-width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background:
            linear-gradient(
                135deg,
                #1476ed,
                #6247e8
            );
        color: white;
        font-weight: 800;
    }

    .workflow-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 15px;
    }

    .workflow-text {
        color: #8fa8c3;
        font-size: 13px;
    }

    .upload-header {
        color: #ffffff;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .upload-description {
        color: #8fa8c3;
        font-size: 13px;
        margin-bottom: 15px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(10, 31, 53, 0.85);
        border: 1px dashed #3c6c9d;
        border-radius: 17px;
        padding: 12px;
    }

    .stButton > button {
        min-height: 50px;
        border-radius: 13px;
        border: 1px solid #3b8be3;
        background:
            linear-gradient(
                90deg,
                #146de1,
                #6247e8
            );
        color: white;
        font-size: 15px;
        font-weight: 750;
        box-shadow: 0 10px 30px rgba(32, 105, 225, 0.25);
    }

    .stButton > button:hover {
        border-color: #8bc9ff;
        box-shadow: 0 14px 35px rgba(32, 105, 225, 0.35);
    }

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #102f52,
                #0a2039
            );
        border: 1px solid #2c527b;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }

    [data-testid="stMetricLabel"] {
        color: #94aec8;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    img {
        border-radius: 14px;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    </style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
  render_html("""
        <div style="font-size:26px; font-weight:800; color:white; margin-bottom:3px;">
            🛰️ Chandrayaan-2
        </div>
    """)

  render_html("""
        <div style="color:#829bb7; font-size:13px; margin-bottom:28px;">
            Multi-Modal Image Correspondence
        </div>
    """)

  render_html("""
        <div style="color:#ffffff; font-size:13px; font-weight:700; margin-bottom:8px;">
            NAVIGATION
        </div>
    """)

  page = st.radio(
      "Navigation",
      ["Home", "Image Upload", "Feature Matching", "Results"],
      label_visibility="collapsed",
  )

  st.markdown("---")

  render_html("""
        <div style="color:#607a97; font-size:12px; line-height:2.4;">
            <b style="color:#829bb7;">SYSTEM</b><br>
            ● Image Processing<br>
            ● ORB Feature Detection<br>
            ● RANSAC Verification<br>
            ● Matching Analysis
        </div>
    """)


# ============================================================
# HOME
# ============================================================

if page == "Home":
  render_html("""
        <div class="main-title">
            Chandrayaan-2 Multi-Modal<br>
            Image Correspondence
        </div>
    """)

  render_html("""
        <div class="subtitle">
            A satellite image analysis platform for discovering
            reliable visual correspondences across Chandrayaan-2 sensors.
        </div>
    """)

  render_html("""
        <div class="hero-card">
            <div class="hero-label">
                SPACE IMAGE INTELLIGENCE
            </div>
            <div class="hero-heading">
                From Lunar Images to Reliable Matches
            </div>
            <div class="hero-description">
                Upload satellite images, enhance them using preprocessing,
                detect ORB features, identify visual correspondences,
                and verify reliable matches using RANSAC.
            </div>
            <br>
            <span class="status-badge">
                ● ORB + Gaussian Blur Baseline Ready
            </span>
        </div>
    """)

  render_html("""
        <div class="section-card">
            <div class="section-title">
                Mission Overview
            </div>
            <div class="section-description">
                The system identifies corresponding regions between
                Chandrayaan-2 satellite images captured by different
                imaging sensors. The workflow combines image preprocessing,
                ORB feature detection, feature matching and geometric
                verification.
            </div>
        </div>
    """)

  col1, col2, col3 = st.columns(3)

  with col1:
    render_html("""
            <div class="feature-card">
                <div class="feature-icon">🖼️</div>
                <div class="feature-title">Image Preprocessing</div>
                <div class="feature-text">
                    Prepare satellite images using Gaussian Blur
                    and image processing techniques before feature detection.
                </div>
            </div>
        """)

  with col2:
    render_html("""
            <div class="feature-card">
                <div class="feature-icon">🔭</div>
                <div class="feature-title">ORB Feature Detection</div>
                <div class="feature-text">
                    Detect distinctive keypoints and generate
                    feature descriptors from satellite imagery.
                </div>
            </div>
        """)

  with col3:
    render_html("""
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">RANSAC Verification</div>
                <div class="feature-text">
                    Verify geometric consistency and identify
                    reliable correspondences from candidate matches.
                </div>
            </div>
        """)

  st.markdown("<br>", unsafe_allow_html=True)

  render_html("""
        <div class="section-card">
            <div class="section-title">
                Processing Pipeline
            </div>
            <br>
            <div class="workflow-card">
                <div class="workflow-number">1</div>
                <div>
                    <div class="workflow-title">Upload Images</div>
                    <div class="workflow-text">Select two satellite images for comparison.</div>
                </div>
            </div>
            <br>
            <div class="workflow-card">
                <div class="workflow-number">2</div>
                <div>
                    <div class="workflow-title">Preprocess Images</div>
                    <div class="workflow-text">Apply Gaussian Blur before feature extraction.</div>
                </div>
            </div>
            <br>
            <div class="workflow-card">
                <div class="workflow-number">3</div>
                <div>
                    <div class="workflow-title">ORB Feature Matching</div>
                    <div class="workflow-text">Detect keypoints and identify candidate correspondences.</div>
                </div>
            </div>
            <br>
            <div class="workflow-card">
                <div class="workflow-number">4</div>
                <div>
                    <div class="workflow-title">RANSAC Verification</div>
                    <div class="workflow-text">Remove geometrically inconsistent matches.</div>
                </div>
            </div>
        </div>
    """)


# ============================================================
# IMAGE UPLOAD
# ============================================================

elif page == "Image Upload":
  render_html("""
        <div class="main-title">Image Upload</div>
        <div class="subtitle">
            Select two Chandrayaan-2 satellite images to begin
            the correspondence analysis.
        </div>
    """)

  col1, col2 = st.columns(2)

  with col1:
    render_html("""
            <div class="section-card">
                <div class="upload-header">🛰️ Reference Image</div>
                <div class="upload-description">Upload the first satellite image.</div>
            </div>
        """)

    uploaded_1 = st.file_uploader(
        "Reference Image",
        type=["png", "jpg", "jpeg", "webp"],
        key="image_upload_1",
        label_visibility="collapsed",
    )

    if uploaded_1 is not None:
      st.session_state.image_1 = uploaded_1.getvalue()
      st.session_state.image_1_name = uploaded_1.name
      st.image(uploaded_1, caption=uploaded_1.name, use_container_width=True)

  with col2:
    render_html("""
            <div class="section-card">
                <div class="upload-header">🌑 Target Image</div>
                <div class="upload-description">Upload the second satellite image.</div>
            </div>
        """)

    uploaded_2 = st.file_uploader(
        "Target Image",
        type=["png", "jpg", "jpeg", "webp"],
        key="image_upload_2",
        label_visibility="collapsed",
    )

    if uploaded_2 is not None:
      st.session_state.image_2 = uploaded_2.getvalue()
      st.session_state.image_2_name = uploaded_2.name
      st.image(uploaded_2, caption=uploaded_2.name, use_container_width=True)

  st.markdown("<br>", unsafe_allow_html=True)

  if st.session_state.image_1 is not None and st.session_state.image_2 is not None:
    st.success("Both images are ready for feature matching.")
    st.info("Go to Feature Matching from the sidebar to run the analysis.")


# ============================================================
# FEATURE MATCHING
# ============================================================

elif page == "Feature Matching":
  render_html("""
        <div class="main-title">Feature Matching</div>
        <div class="subtitle">
            Detect ORB features, generate candidate correspondences,
            and verify them using RANSAC.
        </div>
    """)

  if st.session_state.image_1 is None or st.session_state.image_2 is None:
    st.warning("Please upload both images before running feature matching.")
    st.stop()

  col1, col2 = st.columns(2)

  with col1:
    render_html("""
            <div class="section-card">
                <div class="section-title">Reference Image</div>
            </div>
        """)
    st.image(
        st.session_state.image_1,
        caption=st.session_state.image_1_name,
        use_container_width=True,
    )

  with col2:
    render_html("""
            <div class="section-card">
                <div class="section-title">Target Image</div>
            </div>
        """)
    st.image(
        st.session_state.image_2,
        caption=st.session_state.image_2_name,
        use_container_width=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  run_button = st.button("🚀 Run ORB Matching", use_container_width=True)

  if run_button:
    with st.spinner("Processing images and verifying correspondences..."):
      try:
        result = run_orb_matching(
            st.session_state.image_1, st.session_state.image_2
        )
        st.session_state.matching_result = result
        st.success("Feature matching completed successfully.")
      except Exception as error:
        st.error(f"Matching failed: {error}")

  if st.session_state.matching_result is not None:
    result = st.session_state.matching_result

    st.markdown("<br>", unsafe_allow_html=True)
    render_html("""
            <div class="section-card">
                <div class="section-title">Matching Summary</div>
            </div>
        """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("Image 1 Keypoints", result["keypoints_1"])
    with col2:
      st.metric("Image 2 Keypoints", result["keypoints_2"])
    with col3:
      st.metric("Good Matches", result["good_matches"])
    with col4:
      st.metric("RANSAC Inliers", result["ransac_inliers"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Matching Score", f'{result["matching_score"]:.4f}')

    st.markdown("<br>", unsafe_allow_html=True)
    render_html("""
            <div class="section-card">
                <div class="section-title">Matched Feature Visualization</div>
                <div class="section-description">
                    Candidate ORB correspondences detected between the two satellite images.
                </div>
            </div>
        """)

    matched_image = result["matched_image"]
    matched_image_rgb = cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB)

    st.image(
        matched_image_rgb,
        caption="ORB Feature Correspondences",
        use_container_width=True,
    )


# ============================================================
# RESULTS
# ============================================================

elif page == "Results":
  render_html("""
        <div class="main-title">Analysis Results</div>
        <div class="subtitle">
            Review the feature correspondence and RANSAC verification results.
        </div>
    """)

  if st.session_state.matching_result is None:
    st.info(
        "No analysis results available yet. Upload images and run feature"
        " matching first."
    )
    st.stop()

  result = st.session_state.matching_result

  if result["ransac_inliers"] >= 4:
    st.success("Reliable geometric correspondences detected.")
  else:
    st.warning("Only a small number of RANSAC inliers were detected.")

  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.metric("Keypoints 1", result["keypoints_1"])
  with col2:
    st.metric("Keypoints 2", result["keypoints_2"])
  with col3:
    st.metric("Good Matches", result["good_matches"])
  with col4:
    st.metric("RANSAC Inliers", result["ransac_inliers"])
  with col5:
    st.metric("Matching Score", f'{result["matching_score"]:.4f}')

  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2 = st.columns(2)
  with col1:
    render_html("""
            <div class="section-card">
                <div class="section-title">Reference Image</div>
            </div>
        """)
    st.image(
        st.session_state.image_1,
        caption=st.session_state.image_1_name,
        use_container_width=True,
    )

  with col2:
    render_html("""
            <div class="section-card">
                <div class="section-title">Target Image</div>
            </div>
        """)
    st.image(
        st.session_state.image_2,
        caption=st.session_state.image_2_name,
        use_container_width=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  render_html("""
        <div class="section-card">
            <div class="section-title">Correspondence Visualization</div>
            <div class="section-description">
                Visual representation of detected ORB feature correspondences.
            </div>
        </div>
    """)

  matched_image_rgb = cv2.cvtColor(result["matched_image"], cv2.COLOR_BGR2RGB)
  st.image(matched_image_rgb, caption="ORB Feature Matches", use_container_width=True)

  st.markdown("<br>", unsafe_allow_html=True)

  render_html("""
        <div class="section-card">
            <div class="section-title">Method Configuration</div>
            <div class="section-description">
                <b>Preprocessing:</b> Gaussian Blur<br><br>
                <b>Feature Detector:</b> ORB<br><br>
                <b>Descriptor Matcher:</b> Brute-Force Hamming Distance<br><br>
                <b>Match Filtering:</b> Lowe's Ratio Test (0.75)<br><br>
                <b>Geometric Verification:</b> RANSAC Homography<br><br>
                <b>RANSAC Threshold:</b> 5.0 pixels
            </div>
        </div>
    """)