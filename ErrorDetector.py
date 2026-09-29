import ollama
import os
import json


OLLAMA_url = "http://localhost:11434/api/generate"
model_name = "gemma3:4b-it-qat"
chunk_size = 700  # Characters/chunk, 250-300 words


def analyze_chunk(chunk_text):
    """
    Sends a chunk to the local Ollama instance.
    We ask the model to evaluate the text for language errors.
    """
    prompt = (
         f"INSTRUCTION: Analyze the following academic text for English language errors. "
        f"Provide a structured report with the following sections:\n\n"
        f"1. ERRORS: List all detected errors, numbered, with the original incorrect phrase quoted.\n"
        f"2. SUGGESTED CORRECTIONS: For each error listed above, provide the corrected version.\n"
        f"3. CORRECTED TEXT: The full original text rewritten with all corrections applied.\n"
        f"4. ANALYSIS: Brief summary of the most frequent error types found.\n\n"
        f"TEXT:\n{chunk_text}\n\n"
        f"REPORT:\n"
    )

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1, #low temperature for objectivity, the most LLM possible
            "num_predict": 1000 #600-800 words in the report
        }
    }

    try:
        result = ollama.generate(model=payload["model"], prompt=payload["prompt"], options=payload["options"])
        return result.get("response", "Error: No response from model.")
    except ollama.ResponseError as e:
        return f"Ollama API error: {e.error} (status {e.status_code})"
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"


def main():
    while True:

        #the user personalizes the input file and the report name file
        file_in = input("Introduce the name of your file: ")
        file_out = input("Introduce the name of your report file: ")
        input_file = str(file_in + ".txt")
        output_file = str(file_out + ".txt")

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: {input_file} not found. Please create it first.")
            continue

        # Chunks splitting
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

        #Visualize that the program is running
        print(f"Analysing {len(chunks)} chunks using {model_name}...")

        #report creation
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("AI DETECTION REPORT\n")
            out.write(f"Model used: {model_name}\n")
            out.write(f"Total Chunks: {len(chunks)}\n\n")

            for i, chunk in enumerate(chunks):
                print(f"Analyzing chunk {i + 1}/{len(chunks)}...")
                analysis = analyze_chunk(chunk)

                out.write(f"--- CHUNK {i + 1} ---\n")
                out.write(f"TEXT: {chunk[:100].replace('\n', ' ')}...\n")
                out.write(f"ANALYSIS:\n{analysis.strip()}\n\n")
                out.write("*" * 50 + "\n\n")

        print(f"Analysis complete. Report saved to {output_file}")

        while True:
            q = input("Do you want to continue? [Y/N] ")
            if q.lower() == "y":
                break #break this loop and go back to the main loop
            elif q.lower() == "n":
                print("Exiting...")
                return #ends main
            else:
                print("Invalid input. Please try again.")



if __name__ == '__main__':
    main()