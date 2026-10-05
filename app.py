import os
import tempfile

import gradio as gr
import ollama

# Locally this is http://localhost:11434. In Docker Compose it is set to http://ollama:11434.
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b-it-qat")
CHUNK_SIZE = 700  # characters per chunk (about 250-300 words)

client = ollama.Client(host=OLLAMA_HOST)


def ensure_model():
    """Download the model the first time it is needed (a few GB, so it can take a while)."""
    try:
        client.show(MODEL_NAME)
    except ollama.ResponseError:
        gr.Info(f"Downloading {MODEL_NAME}. This only happens once and can take several minutes.")
        client.pull(MODEL_NAME)
    except Exception as e:
        raise gr.Error(f"Cannot reach Ollama at {OLLAMA_HOST}. Is it running? ({e})")


def analyze_chunk(chunk_text):
    """Send one chunk to Ollama and return the language-error report for it."""
    prompt = (
        "INSTRUCTION: Analyze the following academic text for English language errors. "
        "Provide a structured report with the following sections:\n\n"
        "1. ERRORS: List all detected errors, numbered, with the original incorrect phrase quoted.\n"
        "2. SUGGESTED CORRECTIONS: For each error listed above, provide the corrected version.\n"
        "3. CORRECTED TEXT: The full original text rewritten with all corrections applied.\n"
        "4. ANALYSIS: Brief summary of the most frequent error types found.\n\n"
        f"TEXT:\n{chunk_text}\n\n"
        "REPORT:\n"
    )
    try:
        result = client.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "temperature": 0.1,  # low temperature for objectivity
                "num_predict": 1000,  # roughly 600-800 words in the report
            },
        )
        return result.get("response", "Error: No response from model.")
    except ollama.ResponseError as e:
        return f"Ollama API error: {e.error} (status {e.status_code})"
    except Exception as e:
        return f"Error communicating with Ollama: {e}"


def analyse(file_path, progress=gr.Progress()):
    if file_path is None:
        raise gr.Error("Please upload a .txt file first.")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if not content.strip():
        raise gr.Error("The uploaded file is empty.")

    ensure_model()

    chunks = [content[i:i + CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]

    lines = [
        "LANGUAGE ERROR REPORT",
        f"Model used: {MODEL_NAME}",
        f"Total Chunks: {len(chunks)}",
        "",
    ]

    for i, chunk in enumerate(progress.tqdm(chunks, desc="Analysing chunks")):
        analysis = analyze_chunk(chunk)
        preview = chunk[:100].replace("\n", " ")  # outside the f-string (older Python can't put \n inside one)

        lines += [
            f"--- CHUNK {i + 1} ---",
            f"TEXT: {preview}...",
            f"ANALYSIS:\n{analysis.strip()}\n",
            "*" * 50,
            "",
        ]

    report = "\n".join(lines)

    # essay.txt -> essay_report.txt
    base = os.path.splitext(os.path.basename(file_path))[0]
    out_path = os.path.join(tempfile.mkdtemp(), f"{base}_report.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(report)

    return report, out_path


demo = gr.Interface(
    fn=analyse,
    inputs=gr.File(label="Upload a .txt file", file_types=[".txt"], type="filepath"),
    outputs=[
        gr.Textbox(label="Report preview", lines=20),
        gr.File(label="Download report (.txt)"),
    ],
    title="English Language Error Checker",
    description="Upload a .txt file. The text is split into chunks and each chunk is checked for language errors.",
    flagging_mode="never",
)

# One analysis at a time, so several users don't overload the local model.
demo.queue(default_concurrency_limit=1)

if __name__ == "__main__":
    demo.launch()