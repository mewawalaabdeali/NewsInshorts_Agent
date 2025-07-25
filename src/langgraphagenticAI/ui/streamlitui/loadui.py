import streamlit as st
import os
from src.langgraphagenticAI.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title="🤖💬 News In Short",
            layout="centered",
            initial_sidebar_state="expanded"
        )

        # Serve background.jpg as base64 background
        import base64
        background_path = os.path.abspath("images/background.jpg")
        with open(background_path, "rb") as bg_file:
            bg_encoded = base64.b64encode(bg_file.read()).decode()
        background_style = f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{bg_encoded}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    background-position: center;
                }}
            </style>
        """
        st.markdown(background_style, unsafe_allow_html=True)

        # Embed logo image.png in header
        logo_path = os.path.abspath("images/image.png")
        with open(logo_path, "rb") as logo_file:
            logo_encoded = base64.b64encode(logo_file.read()).decode()

        st.markdown(
            f"""
            <div style='text-align: center; padding: 1rem;'>
                <img src='data:image/png;base64,{logo_encoded}' width='200' style='margin-bottom: 10px;'>
                <h1 style='color: #ffffff; margin-top: 10px;'>News In Short 🚀</h1>
                <p style='font-size: 1.1rem; color: #f0f0f0;'>Empowering your AI workflows with simplicity and power</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.sidebar:
            st.markdown("""
                <style>
                .sidebar .sidebar-content {
                    background-image: linear-gradient(#F0F8FF, #E6F0FA);
                    color: black;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown("## 🌐 Configuration Panel")

            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("💻 Select LLM", llm_options, help="Choose the Large Language Model backend to use")

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("🔧 Select Groq Model", model_options, help="Select one of the Groq-hosted models")
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("🔑 GROQ API Key", type="password", help="Enter your Groq API Key from the developer console")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your GROQ API key to proceed. Don't have one? [Get it here](https://console.groq.com/keys)")

            self.user_controls["selected_usecase"] = st.selectbox("💡 Select Use Case", usecase_options, help="Select the chatbot behavior or mode")

            if self.user_controls["selected_usecase"] == "Chatbot with Web":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("🔑 TAVILY API Key", type="password", help="Required for web-enhanced chatbot use case")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY_API_KEY to proceed.")

        st.markdown("""
            <hr>
            <div style='text-align: center; font-size: 0.85rem; color: #eeeeee;'>
                🌟 Powered by LangGraph + Streamlit UI | Designed by You 🌟
            </div>
        """, unsafe_allow_html=True)

        return self.user_controls
