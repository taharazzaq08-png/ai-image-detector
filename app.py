import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import plotly.express as px
import os

st.set_page_config(page_title="AI vs Real Detector", page_icon="🔍")

@st.cache_resource
def load_model():
    try:
        # Create model
        model = models.efficientnet_b3(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, 2)
        
        # Load weights
        checkpoint = torch.load('EfficientNetB3_best.pth', map_location='cpu')
        
        if isinstance(checkpoint, dict):
            state_dict = checkpoint.get('model_state_dict', checkpoint)
        else:
            state_dict = checkpoint
        
        # Remove 'module.' prefix if present
        new_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith('module.'):
                new_state_dict[k[7:]] = v
            else:
                new_state_dict[k] = v
        
        model.load_state_dict(new_state_dict, strict=False)
        model.eval()
        return model
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((300, 300)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def main():
    st.title("🔍 AI vs Real Image Detector")
    
    model = load_model()
    if model is None:
        st.stop()
    
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        # 👇 ALL these lines MUST be indented (4 spaces)
        # Display image
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption='Uploaded Image', width=400)
        
        # Show progress while analyzing
        with st.spinner("🔬 Analyzing image..."):
            input_tensor = preprocess_image(image)
            with torch.no_grad():
                outputs = model(input_tensor)
                probs = torch.softmax(outputs[0], dim=0)
        
        real_prob, ai_prob = probs[0].item(), probs[1].item()
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Show prediction with color
            if real_prob > ai_prob:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #00b09b, #96c93d); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ REAL</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #ff6b6b, #ee5a24); padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>🤖 AI GENERATED</h2>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Show confidence as metric
            confidence = max(real_prob, ai_prob)
            st.metric("Confidence", f"{confidence:.2%}")
        
        # Add metrics row
        st.markdown("---")
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("Real Probability", f"{real_prob:.2%}", 
                      delta=f"{real_prob-ai_prob:.1%}" if real_prob > ai_prob else None)
        
        with col_m2:
            st.metric("AI Probability", f"{ai_prob:.2%}",
                      delta=f"{ai_prob-real_prob:.1%}" if ai_prob > real_prob else None)
        
        with col_m3:
            st.metric("Decision", "REAL" if real_prob > ai_prob else "AI")
        
        # Add confidence bar
        st.markdown("### Confidence Level")
        if real_prob > ai_prob:
            st.progress(float(real_prob), text=f"Real: {real_prob:.2%}")
        else:
            st.progress(float(ai_prob), text=f"AI: {ai_prob:.2%}")
        
        # Add probability comparison as text
        st.markdown("---")
        st.markdown("### 📊 Probability Breakdown")
        
        # Create a simple HTML bar for visualization
        col_bar1, col_bar2 = st.columns([real_prob*10, ai_prob*10])
        with col_bar1:
            if real_prob > 0:
                st.markdown(f"""
                <div style='background-color: #00b09b; height: 30px; border-radius: 5px; text-align: center; color: white; line-height: 30px;'>
                    Real {real_prob:.1%}
                </div>
                """, unsafe_allow_html=True)
        with col_bar2:
            if ai_prob > 0:
                st.markdown(f"""
                <div style='background-color: #ff6b6b; height: 30px; border-radius: 5px; text-align: center; color: white; line-height: 30px;'>
                    AI {ai_prob:.1%}
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()