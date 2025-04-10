import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pathlib import Path
from PIL import Image
import shutil
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
from app.detector import detect_and_crop
from app.reid import extract_features

st.set_page_config(layout="wide", page_title="Multi-Image Person Matcher AI")
st.title("🧍‍♂️ Multi-Image Person Matcher")
st.caption("Upload multiple images to find people who appear across them.")

# Persistent + Runtime folders
Path("data/crops").mkdir(parents=True, exist_ok=True)
Path("data/labels").mkdir(parents=True, exist_ok=True)
Path("uploads").mkdir(parents=True, exist_ok=True)
Path("runtime_crops").mkdir(parents=True, exist_ok=True)

label_store_path = Path("data/labels/labels.jsonl")

# Dynamic upload key to force reset
if "upload_key" not in st.session_state:
    st.session_state.upload_key = "uploader_1"

# Auto threshold toggle
auto_mode = st.toggle("🔁 Auto Thresholding (90th percentile)", value=True)
manual_threshold = None
if not auto_mode:
    manual_threshold = st.slider("🎚️ Manual Similarity Threshold", 0.0, 1.0, 0.75, 0.01)

# Upload multiple images
uploaded_files = st.file_uploader(
    "📤 Upload Multiple Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key=st.session_state.upload_key
)

# Reset button
if st.button("🔁 Reset (only temporary data)"):
    st.session_state.clear()
    st.session_state.upload_key = f"uploader_{datetime.utcnow().timestamp()}"
    shutil.rmtree("uploads", ignore_errors=True)
    shutil.rmtree("runtime_crops", ignore_errors=True)
    st.rerun()

if uploaded_files:
    all_crops = []
    image_names = []

    for idx, file in enumerate(uploaded_files):
        file_path = f"uploads/image_{idx}.jpg"
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        image_name = file.name
        image_names.append(image_name)

        crops = detect_and_crop(file_path, crop_prefix=f"img{idx}", output_dir="runtime_crops")
        for c in crops:
            c["source"] = image_name
            c["img_idx"] = idx
            all_crops.append(c)

        if crops:
            st.markdown(f"### Detected crops for `{image_name}`")
            crop_cols = st.columns(min(len(crops), 5))
            for i, crop in enumerate(crops):
                crop_cols[i % 5].image(crop["crop_path"], caption=f"Crop {i}", use_container_width=True)
        else:
            st.warning(f"🚫 No people detected in `{image_name}`")

    crop_paths = [c["crop_path"] for c in all_crops]
    st.info(f"🧠 Found {len(crop_paths)} crop(s) to extract features from.")

    features = extract_features(crop_paths)
    st.info(f"🧪 extract_features returned {len(features) if isinstance(features, list) else 'non-list'}")
    features = np.array(features)

    st.text(f"🧪 DEBUG: features type={type(features)}, shape={features.shape}, ndim={getattr(features, 'ndim', 'n/a')}, size={features.size if hasattr(features, 'size') else 'n/a'}")

    if not isinstance(features, np.ndarray):
        st.error("💣 features is not a numpy array")
        st.stop()
    if features.size == 0:
        st.error("💣 features array is empty")
        st.stop()
    if features.ndim != 2:
        st.error(f"💣 features is not 2D: shape={features.shape}")
        st.stop()
    if features.shape[0] < 2:
        st.error("💣 features has <2 rows")
        st.stop()
    if features.shape[1] < 2:
        st.error("💣 features has <2 cols")
        st.stop()

    st.success("✅ Passed all checks. Calculating similarity...")

    try:
        sim_matrix = cosine_similarity(features)
    except Exception as e:
        st.error(f"💥 cosine_similarity failed: {e}")
        st.stop()

    if auto_mode:
        flat_scores = sim_matrix[np.triu_indices_from(sim_matrix, k=1)]
        threshold = np.percentile(flat_scores, 90)
        st.info(f"📊 Auto-selected threshold: {threshold:.2f}")
    else:
        threshold = manual_threshold

    groups = []
    used = set()

    for i in range(len(all_crops)):
        if i in used:
            continue
        group = [i]
        for j in range(i + 1, len(all_crops)):
            if sim_matrix[i][j] >= threshold:
                group.append(j)
                used.add(j)
        used.add(i)
        if len(group) > 1:
            groups.append(group)

    if not groups:
        st.warning("🤔 No visual matches found between people across images.")
    else:
        st.write(f"🧑‍🤝‍🧑 Found {len(groups)} matching group(s):")
        for g_idx, group in enumerate(groups):
            st.markdown(f"#### Group #{g_idx + 1} (sim ≥ {threshold:.2f})")
            cols = st.columns(len(group))
            for i, idx in enumerate(group):
                crop = all_crops[idx]
                cols[i].image(crop["crop_path"], caption=f"{crop['source']} (#{idx})", use_container_width=True)

            with st.expander("✅ Is this group correct?"):
                with st.form(f"group_feedback_{g_idx}"):
                    choice = st.radio("Label this group as:", ["same_person", "different_person"], horizontal=True)
                    submitted = st.form_submit_button("✅ Submit Label")

                    if submitted:
                        timestamp = datetime.utcnow().isoformat()
                        group_id = f"group_{g_idx+1}_{timestamp}"
                        label = choice

                        group_crop_dir = Path(f"data/crops/{group_id}")
                        group_crop_dir.mkdir(parents=True, exist_ok=True)
                        filenames = []

                        for idx in group:
                            src = all_crops[idx]["crop_path"]
                            dest = group_crop_dir / os.path.basename(src)
                            shutil.copy(src, dest)
                            filenames.append(str(dest))

                        entry = {
                            "group_id": group_id,
                            "images": filenames,
                            "label": label,
                            "timestamp": timestamp
                        }

                        with open(label_store_path, "a") as f:
                            f.write(json.dumps(entry) + "\n")

                        st.success(f"📁 Group saved as '{label}' ✅")

            st.markdown("---")
else:
    st.info("👆 Upload at least two images to start matching.")