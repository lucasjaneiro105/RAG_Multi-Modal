![image](https://github.com/user-attachments/assets/9128bc49-4610-442c-805f-f8b35b59add9)

# RAG-MultiModal 🤖

Este projeto implementa um sistema de Resposta Baseada em Recuperação (RAG - Retrieval-Augmented Generation) com suporte multimodal, utilizando Streamlit, LangChain e Docling. Ele permite o upload de diversos tipos de arquivos (PDF, DOCX, PPTX, JPG, PNG) e inicia um chatbot que analisa e responde perguntas com base no conteúdo dos documentos enviados. 

## Visão Geral ⚙️

RAG-MultiModal combina técnicas avançadas de conversão de documentos, divisão de textos e armazenamento vetorial para proporcionar respostas precisas e contextualizadas em interações via chat. Ao processar e converter os arquivos para um formato textual, o sistema utiliza embeddings e uma cadeia conversacional de recuperação para manter o contexto durante toda a conversa. Dessa forma, ele é ideal para análise e interpretação de documentos de diferentes formatos, garantindo uma experiência interativa e multimodal.

## Características Principais

1. **Suporte a múltiplos formatos**: Permite o upload e processamento de arquivos em PDF, DOCX, PPTX, JPG e PNG.
2. **Interface interativa**: Desenvolvida com Streamlit, oferecendo upload de arquivos e chat em tempo real diretamente no navegador.
3. **Armazenamento vetorial eficiente**: Implementado com FAISS para busca por similaridade e recuperação de informações.
4. **Integração com múltiplas APIs**: Compatível com OpenAI (para embeddings) e Groq (para modelagem conversacional) para processamento de linguagem.
5. **Conversação contextualizada**: Mantém o histórico do diálogo e utiliza o contexto dos documentos para gerar respostas precisas.
6. **Modularidade e personalização**: Facilmente adaptável, permitindo ajustes nos prompts, na configuração dos modelos e em outros parâmetros.

## Limitações

- A qualidade das respostas depende da clareza, tamanho e formatação dos documentos processados.
- Algumas dependências do Docling possuem divergências com o Streamlit, ocasionando pequenos problemas, mas nada que interfira diretamente no código.
- Utilizar a embedding de um modelo pago (OpenAI) gera um pequeno custo.
- Por ser uma biblioteca nova e ainda em fase experimental, pode demorar para carregar arquivos dependendo do seu tamanho, podendo levar até minutos somente para carregar.
- O sistema apresentou certa dificuldade para fornecer informações a partir de imagens; entretanto, os desenvolvedores do Docling estão trabalhando em atualizações para melhorar a extração de dados de imagens.

## Observações

- Foi utilizada a embedding de um modelo pago, mas poderia ser utilizada uma do Huggingface sem problemas.
- A FAISS foi escolhida para a vector store por sua rapidez no processamento, mas outras alternativas como Chroma ou Milvus também funcionariam perfeitamente.
- Embora seja possível utilizar um modelo pago como o da OpenAI para a LLM, optei pelo modelo da Groq (Ollama), que apresentou respostas com melhor qualidade.
- Existem outras bibliotecas que lidam com OCR, como o pytesseract, mas na minha experiência a integração e a lógica com o Docling foram mais simples e eficientes.
- Para arquivos pequenos e com o objetivo principal de ler textos e tabelas, o sistema supre a necessidade, considerando que é gratuito e de fácil implementação e entendimento.

## Como Executar

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Instale as dependências**: Certifique-se de ter Python 3.8+ instalado.
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**: Crie um arquivo .env na raiz do projeto com sua chave de API:
```bash
GROQ_API_KEY=<sua-chave-api>
```

4. **Inicie a aplicação:**:
```bash
streamlit run Main.py
```
