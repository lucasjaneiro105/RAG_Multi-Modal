from typing import Iterator, List, Tuple, Optional
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
import os
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# estava com erros do streamlit com algumas libs do docling, isso resolveu:
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TORCH_HOME"] = "./torch_cache"
#

class Splitter:
    def __init__(self):
        self._cache = {}
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        self.embedding = OpenAIEmbeddings()
    
    class DoclingFileLoader(BaseLoader):
        def __init__(self, file_path: str | List[str]) -> None:
            self._file_paths = file_path if isinstance(file_path, list) else [file_path]
            self._converter = DocumentConverter(
                allowed_formats=[
                    InputFormat.PDF,
                    InputFormat.DOCX,
                    InputFormat.IMAGE,
                    InputFormat.PPTX,
                ]
            )

        def load_interator(self) -> Iterator[LCDocument]:
            for source in self._file_paths:
                dl_doc = self._converter.convert(source).document
                text = dl_doc.export_to_markdown()
                yield LCDocument(page_content=text)
    
    def gera_hash(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash
    
    def processamento(self, file_path: str) -> Tuple[str, FAISS]:
        file_hash = self.gera_hash(file_path)
        
        if file_hash in self._cache:
            return file_hash, self._cache[file_hash]['vectorstore']
        
        loader = self.DoclingFileLoader(file_path)
        docs = list(loader.load_interator())
        splits = self.text_splitter.split_documents(docs)
        
        vectorstore = FAISS.from_documents(
            splits,
            self.embedding
        )
        
        self._cache[file_hash] = {
            'vectorstore': vectorstore,
            'memory': ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        }
        
        return file_hash, vectorstore
    
    def chain(self, file_hash: str) -> Optional[ConversationalRetrievalChain]:
        if file_hash not in self._cache:
            return None
        
        cache_entry = self._cache[file_hash]
        llm = ChatGroq(model="llama3-70b-8192")
        
        return ConversationalRetrievalChain.from_llm(
            llm,
            retriever=cache_entry['vectorstore'].as_retriever(),
            memory=cache_entry['memory'],
            combine_docs_chain_kwargs={"prompt": self.prompt()}
        )
    
    def prompt(self) -> PromptTemplate:
        return PromptTemplate.from_template("""
        [Histórico da Conversa]
        {chat_history}
        
        [Contexto Relevante]
        {context}
        
        Com base no histórico acima e no contexto fornecido, responda à pergunta:
        Pergunta: {question}
        Resposta:""")
