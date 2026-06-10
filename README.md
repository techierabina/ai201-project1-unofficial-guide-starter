# The Unofficial Guide — Project 1

---

## Domain

This system covers student reviews of Computer Science professors at the University of Central Oklahoma (UCO). This knowledge is valuable because it captures honest, experience-based opinions about teaching style, grading, exam difficulty, and workload that students actually use to make course decisions. It is hard to find through official channels because UCO's website only lists professor names and credentials it never tells you whether a professor's exams are brutal, whether they respond to emails, or whether their lectures are worth attending.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/359060 |
| 2 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/3010705 |
| 3 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/2876034 |
| 4 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/1767407 |
| 5 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/3038230 |
| 6 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/2955505 |
| 7 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/600661 |
| 8 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/1314642 |
| 9 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/1182070 |
| 10 | Rate My Professors | Student reviews | https://www.ratemyprofessors.com/professor/2624544 |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** My documents are short student reviews, typically 2-4 sentences each. A 300 character chunk is large enough to capture one complete thought or opinion without merging multiple unrelated opinions together. The 50 character overlap ensures that if a key opinion spans a chunk boundary, both adjacent chunks contain enough context to be retrievable. Chunks smaller than 300 characters would risk cutting individual sentences in half, while larger chunks would merge different students' opinions and dilute the semantic signal for retrieval.

**Final chunk count:** 51 chunks across 10 documents

---

## Sample Chunks

**Chunk 1 — Source: mylavarapu_goutam.txt**
```
Dr. Mylavarapu is an intelligent professor who is elite at teaching Data Structures. You are going to learn a lot from this class, but be prepared to work and really focus. Data Structures is not a walk in the park and if you want to learn, you will from this course.
```

**Chunk 2 — Source: hong_sung.txt**
```
The course expectations are always clear. No tests and typically does not meet at every lecture time, but he is available online at all times. This course consisted entirely of self-guided projects made up of a combination of programming and hardware with required creative additions.
```

**Chunk 3 — Source: bihn_michael.txt**
```
He doesn't understand the course material himself, so expect to teach yourself from the textbook or YouTube. Grading takes 3+ weeks. Office hours he prolongs meetings by sharing stories and figuring out material himself before helping you.
```

**Chunk 4 — Source: park_myung_ah.txt**
```
She assigns a $69 zybooks textbook required to pass filled with busywork. She makes simple concepts difficult and is very unorganized. Her tests are way harder than they need to be. Class average was below 60% and she blamed the students.
```

**Chunk 5 — Source: qian_gang.txt**
```
Dr. Qian is very caring and nice. Whenever you have questions he will try his best to help. He explains a lot in lectures so you need to study hard. The project is a bit hard but exams are not very difficult and he grades easy as long as you show effort.
```

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required)

**Production tradeoff reflection:** For this project I used all-MiniLM-L6-v2 because it runs locally on my machine with no API key, no rate limits, and no cost. In a production system I would weigh several tradeoffs: context length (all-MiniLM-L6-v2 is limited to 256 tokens which works fine for short reviews but would fail on longer documents like syllabi or handbooks), multilingual support (if students wrote reviews in other languages I would need a multilingual model like paraphrase-multilingual-MiniLM-L12-v2), accuracy on domain-specific text (a model fine-tuned on academic or review text might retrieve more precisely than a general-purpose model), and latency vs cost (OpenAI's text-embedding-3-small is more accurate but costs money and requires an API call for every query, making it slower and more expensive at scale).

---

## Grounded Generation

**System prompt grounding instruction:**
```
You are a helpful assistant that answers questions about UCO Computer Science professors based ONLY on student reviews provided to you.

STRICT RULES:
- Answer using ONLY the information in the provided documents below.
- If the documents do not contain enough information to answer the question, say exactly: "I don't have enough information on that based on the available reviews."
- Do not use any outside knowledge or make assumptions.
- Always mention which professor you are discussing.
- Keep answers concise and grounded in the reviews.
```

**How source attribution is surfaced in the response:** The retrieved chunk sources are collected programmatically from ChromaDB metadata and displayed in a separate "Retrieved from" field in the Gradio UI. Every response shows which .txt files the answer was drawn from, so the user can trace the answer back to the original professor's review file.

---

## Query Interface

**Input field:** A text box labeled "Your question" where the user types a plain language question about UCO CS professors.

**Output fields:**
- "Answer" : a multi-line text box showing the grounded response generated by Groq's llama-3.3-70b-versatile model
- "Retrieved from" : a text box listing the source .txt files that were used to generate the answer

**Sample interaction:**

Question: `Is Gang Qian responsive to student questions outside of class?`

Answer: `Based on the reviews, Professor Gang Qian is responsive to student questions outside of class. Review 1 states that he responds quickly outside of class and Review 4 mentions that he always answers questions quickly and provides great feedback.`

Retrieved from:
```
- qian_gang.txt
- mylavarapu_goutam.txt
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Dr. Mylavarapu's exams? | Exams can tank your grade if you don't follow lectures and take notes | Exams can tank your grade if you didn't follow lectures and take notes, implying they are challenging if unprepared | Relevant | Accurate |
| 2 | Does Hong Sung give tests in his classes? | No tests or quizzes, grades based entirely on projects | Professor Hong Sung typically does not give tests in his CMSC4313 class | Relevant | Accurate |
| 3 | How is Michael Bihn's teaching style described by students? | Reads off slides in monotone voice, doesn't know material, students must teach themselves | Teaching style is described as poor — doesn't understand course material, technical issues with Zoom recordings | Relevant | Accurate |
| 4 | What do students say about Myung-Ah Park's difficulty level? | Unnecessarily difficult, very hard tests weighted heavily, recommend Mylavarapu instead | Makes simple concepts difficult, tests harder than needed, class average below 60%, coding assignments above class level | Relevant | Accurate |
| 5 | Is Gang Qian responsive to student questions outside of class? | Yes, responds quickly and is always available | Yes, responds quickly outside of class and always answers questions quickly | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** "How is Michael Bihn's teaching style described by students?"

**What the system returned:** The top result was correctly from bihn_michael.txt (distance: 0.756), but the second and third results were pulled from hong_sung.txt and qian_gang.txt with distances above 1.0. These chunks mentioned "monotone voice" and "lecture videos" which semantically overlapped with Bihn's reviews even though they were about different professors.

**Root cause (tied to a specific pipeline stage):** This is a retrieval stage issue. Because our chunks are only 300 characters, some chunks don't include the professor's name, they only contain the review text. When the embedding model encodes a chunk like "reads off slides in a low monotone voice," it has no professor identity attached. So when a query about Bihn is made, chunks from other professors with similar complaints score as semantically close even though they are about different people.

**What you would change to fix it:** Prepend the professor's name to every chunk before embedding, so every vector carries professor identity as part of its meaning. For example: "Professor Michael Bihn: reads off slides in a low monotone voice..." This would push unrelated professor chunks further away in vector space.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before coding forced me to think about the structure of my documents before writing any code. Because I had already decided on 300 character chunks with 50 character overlap and written down the reasoning, I could implement ingest.py directly from the spec without guessing. The spec also served as a prompt to Claude when generating the pipeline code, which produced more accurate results than a vague request would have.

**One way your implementation diverged from the spec, and why:** In planning.md I anticipated that chunk boundary splitting would be the main challenge. In practice, a bigger issue emerged during retrieval testing chunks from different professors were being retrieved together because similar complaints appear across multiple professors. This cross-professor retrieval problem was not anticipated in the spec. If I were to revise the spec, I would add a metadata filtering step that prepends professor names to chunks before embedding to preserve professor identity in the vector space.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Domain section, Documents section, and Chunking Strategy section from planning.md, and asked Claude to implement ingest.py that loads all 10 .txt files and splits into 300 character chunks with 50 character overlap.
- *What it produced:* A complete ingest.py with load_documents(), chunk_text(), and ingest() functions using fixed character splitting with the specified chunk size and overlap.
- *What I changed or overrode:* I verified the output by running python3 ingest.py and printing 5 sample chunks. The chunks looked correct and self-contained so I kept the implementation as generated.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section, Architecture diagram, and grounding requirement from planning.md, and asked Claude to implement app.py with a Groq generation function and Gradio UI that enforces answers from retrieved context only.
- *What it produced:* A complete app.py with a strict system prompt, context formatting from retrieved chunks, source attribution collected programmatically from ChromaDB metadata, and a Gradio UI with question input and answer/sources output fields.
- *What I changed or overrode:* I tested an out-of-scope question and confirmed the system correctly refused to answer rather than hallucinating, verifying the grounding instruction was working as specified.