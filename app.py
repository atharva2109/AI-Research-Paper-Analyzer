import json
from flask import Flask, render_template, request, jsonify
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

from sympy import sec
from src.RAG_retrieval_chain import get_qa_chain
from src.create_vector_db import create_vector_db
from src.generate_summary import generate_detailed_summary
from src.load_and_extract_text import extract_text_from_pdf,extract_pdf_sections
from src.detect_and_split_sections import refine_section, split_sections_with_content


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
full_text=''
vector_db=None
load_dotenv()
Research_paper_with_topics=None
groq_api_key=os.getenv("GROQ_API_KEY")
embedding_model=os.getenv("EMBEDDING_MODEL")
llm_model=os.getenv("LLM_MODEL")

llm=ChatGroq(model=llm_model, api_key=groq_api_key)
# print(llm.invoke("Which is more faster language, C++ or Python?"))

embedding=HuggingFaceEmbeddings(model_name=embedding_model)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file=request.files['file']
    global full_text
    global Research_paper_with_topics
    if not file:
        return jsonify({"error":"No file uploaded"}), 400

    file_name=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_name)
    extracted_text=extract_text_from_pdf(file_name)
    full_text=extracted_text
    extracted_sections=extract_pdf_sections(full_text=extracted_text)
    refined_sections=refine_section(extracted_sections,llm)
    sections_with_content=split_sections_with_content(extracted_text,refined_sections)
    Research_paper_with_topics=sections_with_content
    return jsonify({"topics": list(Research_paper_with_topics.keys())})

@app.route("/summary", methods=['POST'])
def get_summary():
    global Research_paper_with_topics

    topic=request.json.get("topic")
    topic_content=Research_paper_with_topics.get(topic,"No summary available for this topic.")
    summary=generate_detailed_summary(topic_content,llm)

    return jsonify({"summary": summary})

@app.route("/chat",methods=['POST'])
def chat():
    global full_text
    global vector_db
    user_message=request.json.get("message")
    
    if not vector_db:
        vectordb=create_vector_db(full_text,embedder=embedding)
        vector_db=vectordb
    
    chain=get_qa_chain(vector_db,llm)
    ai_response=chain.invoke(user_message)["result"]

    return jsonify({"response":ai_response})

if __name__ == "__main__":
    app.run(debug=True)
    # extracted_text=extract_text_from_pdf("paper.pdf")
    # # print(extracted_text[:500])
    # extracted_sections=extract_pdf_sections(extracted_text)
    # # with open("extracted.json","w") as f:
    # #     json.dump(extracted_sections,f,indent=4)
    # refined_sections=refine_section(extracted_sections,llm)
    # # with open("refined_sections.json","w") as f:
    # #     json.dump(refined_sections,f,indent=4)
    # section_with_content=split_sections_with_content(extracted_text,refined_sections)
    # with open("section_with_content.json","w") as f:
    #     json.dump(section_with_content,f,indent=4)
