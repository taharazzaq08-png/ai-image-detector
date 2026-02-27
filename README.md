# AI Image Detector

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-blue)](https://huggingface.co/spaces/Mina009/ai-image-d)
[![GitHub](https://img.shields.io/badge/GitHub-Code-black)](https://github.com/taharazzaq08-png/ai-image-detector)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

## 🎯 Try It Live!
**[Click here to test the app on Hugging Face](https://huggingface.co/spaces/Mina009/ai-image-d)** 
No installation needed - works directly in your browser!

## 📝 Overview
An AI-powered application that detects whether images are real photographs or AI-generated.

## ✨ Features
- Upload images (JPG, PNG, etc.)
- Real-time prediction with confidence scores
- Interactive visualizations using Plotly
- Clean web interface built with Streamlit

## 🚀 Local Installation

### Prerequisites
- Python 3.8 or higher


### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-github-username/your-repo-name.git
   cd your-repo-name
   
Install dependencies

```bash
pip install -r requirements.txt
```
Run the app

```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser

🐳 Run with Docker
```bash
docker build -t ai-detector .
docker run -p 8501:8501 ai-detector
```
📦 Dependencies
```text
streamlit==1.28.1 - Web app framework

pillow==10.0.1 - Image processing

numpy==1.24.3 - Numerical operations

plotly==5.17.0 - Interactive visualizations
```

📁 Project Structure
```text
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


