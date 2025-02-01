import streamlit as st
from Utils import Splitter
import tempfile
import os

def reset_session():
    st.session_state.clear()

def main():
    st.markdown(
        "<h1 style='text-align: center; color: black;'>RAG-MultiModal ⚙️🧠</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='text-align: center; color: black;'>Feito com Docling 🐥</h4>",
        unsafe_allow_html=True
    )
    

    if 'rag' not in st.session_state:
        st.session_state.rag = Splitter()
        st.session_state.active_arquivo_hash = None
    

    with st.sidebar:
        uploaded_file = st.file_uploader(
            "Adicione seu arquivo 📂",
            type=["pdf", "docx", "pptx", "jpg", "png"],
            on_change=reset_session
        )
    
    if uploaded_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            file_hash, vectorstore = st.session_state.rag.processamento(file_path)
            st.session_state.active_arquivo_hash = file_hash
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Faça sua pergunta"):
        if not uploaded_file:
            st.error("Por favor, carregue algum documento")
            return
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Processando sua pergunta ⌛"):
            try:
                chain = st.session_state.rag.chain(
                    st.session_state.active_arquivo_hash
                )
                
                response = chain.invoke({
                    "question": prompt,
                    "chat_history": st.session_state.messages
                })
                
                answer = response["answer"]
                
            except Exception as e:
                answer = f"Erro ao processar a pergunta: {str(e)}"
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
