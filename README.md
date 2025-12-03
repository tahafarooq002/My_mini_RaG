# RAG Assistant


A **Overview of the **RAG Assistant** workflow.  
- Documents are first **chunked** and stored with **FAISS embeddings**.  
- User queries are either **typed or spoken** (STT).  
- The assistant **retrieves relevant chunks** from the knowledge base.  
- Retrieved context is fed to the **language model** (OpenAI / Bytez / HuggingFace).  
- The **answer is generated**, displayed, and optionally spoken via **TTS**.  
- The system supports **actions**, like opening websites or other automated tasks.




---

## Features

1. **RAG (Retrieval-Augmented Generation)**
   - Retrieves relevant information from documents using **FAISS**.
   - Generates precise answers using **HuggingFace/OpenAI APIs**.

2. **Text-to-Speech (TTS)**
   - Converts assistant responses to voice using **gTTS**.
   - Works safely in loops, notebooks, and scripts.

3. **Speech-to-Text (STT)**
   - Listen to your voice queries using **Google Speech Recognition**.

4. **Document Chunking**
   - Automatically splits large documents into smaller passages.
   - Supports multiple text files for retrieval.

5. **Interactive Notebook Support**
   - Run `assistant_notebook.ipynb` for interactive queries and responses.

6. **Action Execution**
   - Open websites or perform simple Python-based actions.

---

## **Directory Structure**
```
RAG-Assistant/
├── assistant/
│ ├── init.py
│ ├── tts.py # Text-to-Speech
│ ├── stt.py # Speech-to-Text
│ ├── rag.py # RAG + FAISS + API integration
│ ├── action.py # Actions like open website
├── notebooks/
│ ├── assistant_notebook.ipynb
│ ├── docs.ipynb # Chunk documents & build FAISS index
├── index/ # FAISS index & metadata
│ ├── faiss.index
│ └── meta.json
├── requirements.txt
├── README.md
```


---

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd RAG-Assistant
```
2. **Create a conda environment**
```bash
conda create -n ai_assistant python=3.10 -y
conda activate ai_assistant
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
## Document Setup

You need text documents (books or manuals) to build the knowledge base.

**.** Example: Pride and Prejudice
Download from Project Gutenberg

**.** Place text files in a folder, e.g., documents/.

**.** Run notebooks/docs.ipynb to:

    1. Chunk the text into smaller passages.

    2. Generate embeddings using SentenceTransformer.

    3. Build FAISS index and save meta.json.

After running, you will have:
```bash
index/faiss.index
index/meta.json
```

## Configuration

1. **Set HuggingFace/OpenAI API token**
```bash
export HF_TOKEN="your_huggingface_or_openai_api_key"
```

2. **Optional:** Update assistant/rag.py to use your preferred model.

## **Usage**

**Run in Notebook**

**.** Open notebooks/assistant_notebook.ipynb.

**.** Ask questions interactively and listen to answers.

## **Supported Documents**

**.** Free books from Project Gutenberg

**.** Text manuals or PDFs converted to .txt

## **Example**
**Input Query:**
```csharp
Who is Elizabeth Bennet?
```
**Output:**
```vbnet
Answer: Elizabeth Bennet is the main character in Pride and Prejudice.
Sources: ['pride_and_prejudice.txt']
```
  **TTS: Reads out the answer automatically.**

  ## **Notes**
  
  **.** Works best with Python 3.10+

  **.** Ensure index/faiss.index and index/meta.json exist before running.

  **.**  gTTS requires an internet connection for TTS.
