import os
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve
import gradio as gr

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    chunks = retrieve(question, k=4)
    
    context = ""
    sources = []
    for chunk in chunks:
        context += f"Source: {chunk['source']}\n{chunk['text']}\n\n"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])

    system_prompt = """You are a helpful assistant that answers questions about UCO Computer Science professors based ONLY on student reviews provided to you.

STRICT RULES:
- Answer using ONLY the information in the provided documents below.
- If the documents do not contain enough information to answer the question, say exactly: "I don't have enough information on that based on the available reviews."
- Do not use any outside knowledge or make assumptions.
- Always mention which professor you are discussing.
- Keep answers concise and grounded in the reviews."""

    user_message = f"""Documents:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    answer = response.choices[0].message.content
    return {"answer": answer, "sources": sources}

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="UCO CS Professor Guide") as demo:
    gr.Markdown("# UCO CS Unofficial Professor Guide")
    gr.Markdown("Ask anything about UCO Computer Science professors based on student reviews.")
    inp = gr.Textbox(label="Your question", placeholder="e.g. Does Hong Sung give tests?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()