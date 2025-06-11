import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
import time

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

fs = FewShotPosts()
tags = fs.get_tags()

def main():
    local_css("style.css")
    
    st.image("https://cdn-icons-png.flaticon.com/512/174/174857.png", width=80)
    st.title("LinkedIn Post Generator")
    st.markdown("Create engaging LinkedIn posts in seconds with AI")
    
    with st.container():
        st.markdown("""
        <div class="container">
            <div class="header">
                <h3>Customize Your Post</h3>
            </div>
            <div class="content">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_tag = st.selectbox(
                "🎯 Select Topic", 
                options=tags,
                help="Choose a topic for your LinkedIn post"
            )
        
        with col2:
            selected_length = st.selectbox(
                "📏 Post Length", 
                options=["Short", "Medium", "Long"],
                help="Select how long you want your post to be"
            )
        
        with col3:
            selected_language = st.selectbox(
                "🌐 Language", 
                options=["English", "Tanglish"],
                help="Choose your preferred language"
            )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    if st.button("✨ Generate Post", key="generate"):
        with st.spinner("Generating your perfect post..."):
            time.sleep(1)
            
            post = generate_post(selected_length, selected_language, selected_tag)
            
            st.markdown("""
            <div class="post-container">
                <div class="post-header">
                    <h3>Your Generated Post</h3>
                </div>
                <div class="post-content">
            """, unsafe_allow_html=True)
            
            st.write(post)
            
            st.markdown("""
                </div>
                <div class="post-actions">
                    <button class="copy-btn" onclick="navigator.clipboard.writeText(`""" + post.replace("`", "'") + """`)">📋 Copy to Clipboard</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()