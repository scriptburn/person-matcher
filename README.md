# 🧍‍♂️ Person Matcher AI

A Streamlit-based AI tool that detects and matches people across multiple images taken from different angles or devices — ideal for tourist photos at places like the Taj Mahal.

[![License: Non-Commercial](https://img.shields.io/badge/license-non--commercial-blue.svg)](LICENSE)

---

## ✨ Features

- 📤 Upload multiple images
- 🧠 Detect people using YOLOv8
- 🧬 Extract features via TorchReID
- 📈 Visual match grouping based on cosine similarity
- 🧮 Auto or manual thresholding
- ✅ Label match results as correct/incorrect
- 📦 Save labeled pairs for training dataset
- 📁 Export dataset for COCO/CSV training
- 🐳 Dockerized with Makefile for easy dev/prod workflows

---

## 🖼️ Use Case

> Given Image A and Image B taken at the same place by two different people, the app identifies if both images contain the same individual — even from different angles or cameras.

---

## 🚀 Run Locally (Dev Mode)

```bash
make build
make dev
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 🏗️ Project Structure

```
person-matcher/
├── app/
│   ├── detector.py      # Person detection (YOLOv8 or simulated)
│   ├── reid.py          # Feature extraction and re-ID
├── web/
│   └── app.py           # Streamlit frontend
├── data/
│   ├── crops/           # Saved validated crop pairs
│   └── labels/          # labels.jsonl with group metadata
├── uploads/             # Temp uploaded images
├── runtime_crops/       # Temp detection results
├── Dockerfile
├── Makefile
├── requirements.txt
└── .gitignore
```

---

## 📦 Dataset Workflow

1. Upload multiple images
2. Confirm visually matched people
3. Save labeled data
4. Export dataset for training

---

## 📤 Exporting

- Export labeled dataset to COCO or CSV for training (coming soon)
- Future: `make export-coco` or `make export-csv`

---

## 🧪 Tech Stack

- Streamlit
- YOLOv8 (Ultralytics)
- TorchReID
- NumPy + Scikit-learn
- Docker + Makefile

---

## 📜 License

This project is licensed for **non-commercial use only**.

If you wish to use this software in a commercial product or service, please contact the author

---

## 👩‍💻 Author

Created by [Your Name] — a passionate AI + Web developer from India 🇮🇳  
Drop a ⭐ if this project helped you!

---

## 📄 License File

See the [LICENSE](LICENSE) file in this repository for full details.
