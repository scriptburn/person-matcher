# 👤 Person Matcher AI

This app detects and matches people across two images taken at the same location from different perspectives using YOLOv8 and TorchReID.

### 🧠 Features

- Detect people using YOLOv8
- Re-identify people using TorchReID (OSNet)
- Streamlit-based UI
- Dockerized for easy deployment

---

### 🚀 Run via Docker

```bash
git clone https://github.com/your-username/person-matcher.git
cd person-matcher
docker build -t person-matcher .
docker run -p 8501:8501 person-matcher
```

---

### 🧪 Sample Use Case

Use this to match friends taking pictures at the Taj Mahal from different angles or in crowded tourist places.

---

### 📁 Folder Structure

project-root/
├── Dockerfile
├── requirements.txt
├── web/          # Streamlit app
├── app/          # Detection + ReID logic
├── models/       # YOLO weights
├── crops/        # Auto-generated crops
└── uploads/      # Uploaded files

---

### 📝 Credits

- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [TorchReID](https://github.com/KaiyangZhou/deep-person-reid)
