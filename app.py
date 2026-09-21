import random
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
            radial-gradient(circle at 85% 5%, rgba(39, 112, 190, 0.28), transparent 30%),
            radial-gradient(circle at 10% 85%, rgba(25, 72, 125, 0.20), transparent 35%),
            linear-gradient(135deg, #02060f 0%, #061324 45%, #07172b 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020813 0%, #05111f 55%, #030c17 100%);
        border-right: 1px solid rgba(75, 145, 210, 0.25);
    }

    .main-title {
        font-size: 40px;
        line-height: 1.12;
        font-weight: 850;
        letter-spacing: -1.2px;
        background: linear-gradient(90deg, #ffffff 0%, #dceeff 40%, #52abff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .subtitle {
        color: #c2d4e8;
        font-size: 16px;
        line-height: 1.65;
        margin-bottom: 28px;
        max-width: 900px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }

    .hero-banner {
        position: relative;
        border: 1px solid rgba(80, 150, 225, 0.4);
        border-radius: 22px;
        padding: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
    }

    .section-card {
        background: linear-gradient(145deg, rgba(16, 38, 64, 0.90), rgba(8, 23, 42, 0.92));
        padding: 24px;
        border-radius: 18px;
        border: 1px solid rgba(69, 115, 157, 0.35);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    .preview-box {
        background: rgba(10, 25, 45, 0.7);
        border: 2px dashed rgba(60, 110, 160, 0.4);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        color: #8fa8c3;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: 1px solid #3b8be3;
        background: linear-gradient(90deg, #146de1, #6247e8);
        color: white;
        font-size: 15px;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(32, 105, 225, 0.3);
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #102f52, #0a2039);
        border: 1px solid #2c527b;
        padding: 12px;
        border-radius: 14px;
    }

    #MainMenu, footer { visibility: hidden; }
    </style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
  render_html("""
        <div style="font-size:22px; font-weight:800; color:white; margin-bottom:2px;">
            🛰️ Chandrayaan-2
        </div>
        <div style="color:#829bb7; font-size:11px; margin-bottom:24px;">
            Image Correspondence
        </div>
        <div style="color:#ffffff; font-size:11px; font-weight:700; margin-bottom:6px; letter-spacing:1px;">
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
        <div style="color:#607a97; font-size:11px; line-height:2.2;">
            <b style="color:#829bb7;">SYSTEM INFO</b><br>
            ● ORB Detection Active<br>
            ● RANSAC Ready<br>
            ● UI Version 2.0
        </div>
    """)


# ============================================================
# HOME PAGE (WITH DYNAMIC MOON/SPACE BACKGROUND BEHIND TEXT)
# ============================================================

if page == "Home":
  # List of 10 Moon + Space Dark Theme Images
  space_images = [
      (
          "https://images.unsplash.com/photo-1522030299830-16b8d3d049fe?auto=format&fit=crop&w=1200&q=80",
          "Lunar Surface & Deep Space",
      ),
      (
          "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?auto=format&fit=crop&w=1200&q=80",
          "Interstellar Deep Star Field",
      ),
      (
          "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&w=1200&q=80",
          "Milky Way Galaxy Horizon",
      ),
      (
          "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
          "Planet Earth from Orbit",
      ),
      (
          "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?auto=format&fit=crop&w=1200&q=80",
          "Lunar Crater Topography",
      ),
      (
          "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?auto=format&fit=crop&w=1200&q=80",
          "Deep Space Nebula Cluster",
      ),
      (
          "https://images.unsplash.com/photo-1538370965046-79c0d6907d47?auto=format&fit=crop&w=1200&q=80",
          "Full Moon Detailed Texture",
      ),
      (
          "https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&w=1200&q=80",
          "Cosmic Dust & Star Systems",
      ),
      (
          "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
          "Abstract Space Light Spectrum",
      ),
      (
          "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1200&q=80",
          "Orbital Satellite View",
      ),
  ]

  # Randomly pick one image for the hero background on reload
  bg_url, bg_caption = random.choice(space_images)

  render_html(f"""
        <div class="hero-banner" style="background-image: linear-gradient(135deg, rgba(3, 9, 23, 0.92) 0%, rgba(6, 23, 43, 0.85) 100%), url('{bg_url}');">
            <span style="background: rgba(40, 180, 120, 0.25); border: 1px solid rgba(50, 220, 150, 0.5); color: #5eead4; padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                ● Live Background: {bg_caption}
            </span>
            <div class="main-title" style="margin-top: 15px;">
                Chandrayaan-2 Multi-Modal<br>Image Correspondence Platform
            </div>
            <div class="subtitle">
                Advanced lunar imagery analysis system designed to discover, map, and verify visual correspondences across multi-sensor Chandrayaan-2 payload data.
            </div>
            <p style="color: #e2e8f0; font-size: 14px; line-height: 1.6; max-width: 750px; margin-bottom: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">
                Leverage high-performance computer vision pipelines combining Gaussian filtering, ORB feature extraction, and RANSAC geometric verification to align satellite imagery seamlessly.
            </p>
        </div>
    """)

  col1, col2, col3 = st.columns(3)

  with col1:
    render_html("""
            <div class="section-card" style="height: 100%;">
                <div style="font-size: 28px; margin-bottom: 10px;">🖼️</div>
                <h4 style="color: white; margin-top: 0; margin-bottom: 8px; font-size: 16px;">1. Image Preprocessing</h4>
                <p style="color: #9fb6cf; font-size: 13px; line-height: 1.5; margin-bottom: 0;">
                    Enhance raw lunar surface data using Gaussian Blur and precise image normalization filters to eliminate sensor noise.
                </p>
            </div>
        """)

  with col2:
    render_html("""
            <div class="section-card" style="height: 100%;">
                <div style="font-size: 28px; margin-bottom: 10px;">🔍</div>
                <h4 style="color: white; margin-top: 0; margin-bottom: 8px; font-size: 16px;">2. ORB Feature Detection</h4>
                <p style="color: #9fb6cf; font-size: 13px; line-height: 1.5; margin-bottom: 0;">
                    Detect robust keypoints and generate rotation-invariant binary descriptors to establish accurate point matches.
                </p>
            </div>
        """)

  with col3:
    render_html("""
            <div class="section-card" style="height: 100%;">
                <div style="font-size: 28px; margin-bottom: 10px;">🛡️</div>
                <h4 style="color: white; margin-top: 0; margin-bottom: 8px; font-size: 16px;">3. RANSAC Verification</h4>
                <p style="color: #9fb6cf; font-size: 13px; line-height: 1.5; margin-bottom: 0;">
                    Filter out false outliers and validate geometric consistency using robust homography estimation models.
                </p>
            </div>
        """)


# ============================================================
# IMAGE UPLOAD PAGE
# ============================================================

elif page == "Image Upload":
  render_html("""
        <div class="main-title">Upload Satellite Images</div>
        <div class="subtitle">Upload two satellite images to compare their visual correspondence.</div>
    """)

  col1, col2 = st.columns(2)

  with col1:
    render_html("""
            <div style="font-weight:700; color:white; margin-bottom:6px; font-size:14px;">🔵 1. Upload First Image</div>
        """)
    uploaded_1 = st.file_uploader(
        "Upload First Image",
        type=["png", "jpg", "jpeg", "webp"],
        key="u1",
        label_visibility="collapsed",
    )
    if uploaded_1 is not None:
      st.session_state.image_1 = uploaded_1.getvalue()
      st.session_state.image_1_name = uploaded_1.name

  with col2:
    render_html("""
            <div style="font-weight:700; color:white; margin-bottom:6px; font-size:14px;">🟣 2. Upload Second Image</div>
        """)
    uploaded_2 = st.file_uploader(
        "Upload Second Image",
        type=["png", "jpg", "jpeg", "webp"],
        key="u2",
        label_visibility="collapsed",
    )
    if uploaded_2 is not None:
      st.session_state.image_2 = uploaded_2.getvalue()
      st.session_state.image_2_name = uploaded_2.name

  st.markdown("<br>", unsafe_allow_html=True)
  render_html("""
        <div style="font-weight:700; color:white; margin-bottom:10px; font-size:15px;">🖼️ Preview Images</div>
    """)

  p_col1, p_col2 = st.columns(2)
  with p_col1:
    if st.session_state.image_1 is not None:
      st.image(
          st.session_state.image_1,
          caption=f"Image 1: {st.session_state.image_1_name}",
          width=500,
      )
    else:
      render_html(
          '<div class="preview-box">📷 No image selected<br><span'
          ' style="font-size:11px; color:#556b82;">Upload First'
          " Image</span></div>"
      )

  with p_col2:
    if st.session_state.image_2 is not None:
      st.image(
          st.session_state.image_2,
          caption=f"Image 2: {st.session_state.image_2_name}",
          width=500,
      )
    else:
      render_html(
          '<div class="preview-box">📷 No image selected<br><span'
          ' style="font-size:11px; color:#556b82;">Upload Second'
          " Image</span></div>"
      )


# ============================================================
# FEATURE MATCHING PAGE
# ============================================================

elif page == "Feature Matching":
  render_html("""
        <div class="main-title">Feature Matching</div>
        <div class="subtitle">Detect keypoints, match features and verify using RANSAC.</div>
    """)

  render_html("""
        <div class="section-card">
            <h4 style="color:white; margin-top:0; font-size:16px;">Matching Parameters</h4>
        </div>
    """)

  m1, m2, m3 = st.columns(3)
  with m1:
    st.selectbox("Feature Detector", ["ORB"])
  with m2:
    st.selectbox("Matcher", ["BFMatcher (Hamming)"])
  with m3:
    st.number_input("RANSAC Threshold", value=5.0)

  st.markdown("<br>", unsafe_allow_html=True)
  run_btn = st.button("🚀 Run Matching")

  if run_btn:
    if st.session_state.image_1 is None or st.session_state.image_2 is None:
      st.warning(
          "⚠️ Please upload two images first from the 'Image Upload' section"
          " before running matching."
      )
    else:
      with st.spinner("Processing matching algorithm..."):
        try:
          res = run_orb_matching(
              st.session_state.image_1, st.session_state.image_2
          )
          st.session_state.matching_result = res
          st.success("Matching completed successfully! Go to Results page.")
        except Exception as e:
          st.error(f"Error during matching: {e}")


# ============================================================
# RESULTS PAGE
# ============================================================

elif page == "Results":
  render_html("""
        <div class="main-title">Matching Results</div>
        <div class="subtitle">View the matching results, keypoints and analysis.</div>
    """)

  if st.session_state.matching_result is None:
    render_html("""
            <div class="section-card" style="text-align:center; padding: 30px;">
                <h4 style="color:#ffcc00; margin-top:0;">⚠️ No results yet</h4>
                <p style="color:#8fa8c3; font-size:13px;">Run the matching process from the Feature Matching page to see the results here.</p>
            </div>
        """)
  else:
    res = st.session_state.matching_result

    r_col1, r_col2 = st.columns([2, 1])

    with r_col1:
      render_html("""
                <div class="section-card">
                    <h4 style="color:white; margin-top:0; font-size:16px;">Visual Correspondence</h4>
                </div>
            """)
      matched_rgb = cv2.cvtColor(res["matched_image"], cv2.COLOR_BGR2RGB)
      st.image(
          matched_rgb, caption="ORB Correspondence Matches", width=700
      )

    with r_col2:
      render_html("""
                <div class="section-card">
                    <h4 style="color:white; margin-top:0; font-size:16px;">Matching Summary</h4>
                </div>
            """)
      st.metric("Keypoints (Image 1)", res["keypoints_1"])
      st.metric("Keypoints (Image 2)", res["keypoints_2"])
      st.metric("Good Matches", res["good_matches"])
      st.metric("Matching Score", f"{res['matching_score']:.3f}")