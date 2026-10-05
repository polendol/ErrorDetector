# Error Detector

## Description
This error detector uses Gemma model to detect English errors in writing of any .txt file within the project and 
generates report (.txt file) by chunks listing errors and corrections. As academic papers in preparation are privacy-sensitive, 
this program has been created to facilitate error detection during text editing without submitting the documents online
for error detection prior to publication. This model is run locally through Ollama and requires pulling `gemma3:4b-it-qat`.

The text is analysed by chunks of 700 characters (100 words), to imitate the
average paragraph size of the text.

The input files must be .txt files. Report is generated as .txt file within the same project. 

## Docker
### Requirements
1. **Docker:** Installed and running (Docker Desktop on Windows/macOS or Docker Engine on Linux).
2. **Docker Compose:** Included by default with Docker Desktop, or available via the `docker-compose-plugin`.
3. **Hardware:** Minimum 8 GB RAM recommended. At least 10 GB of free disk space for the Ollama image, the `gemma3:4b-it-qat` model weights (about 4 GB), and the Python base image layers.
4**Internet:** Required on the first run only, to download the Ollama image and the model. After that, everything runs locally and offline.

### How it works
1. **Two containers:** Docker Compose starts an `ollama` container (the language model server) and an `app` container (the Gradio web interface). The app starts only once Ollama is ready.
2. **Web interface:** The app runs on port 7860. You upload a `.txt` file in your browser and download the report from the same page. No `data/` folder needs to be created or mounted.
3. **Reports:** Each report is shown on the page and offered as a `.txt` download named after your file (e.g. `my_essay.txt` becomes `my_essay_report.txt`). Reports are not stored on your computer unless you download them.
4. **Ollama model cache:** The `gemma3:4b-it-qat` model (~4 GB) is downloaded automatically the first time you run an analysis, and cached in a named Docker volume (`ollama_data`). It is downloaded only once and reused afterwards.

### Step by step
1. Build and start the application:`docker compose up --build`
2. Wait until the logs show that Gradio is running.
3. Open http://localhost:7860 in your browser.
4. Upload a `.txt` file. On the very first analysis the model is downloaded first, so expect a few minutes of waiting. A progress bar then tracks the chunks.
5. Read the report on the page or click the download link to save it.

## Local
## Requirements
- Python 3.8+
- [Ollama](https://ollama.com) running locally
- Model: `gemma3:4b-it-qat` pulled in Ollama

## Installation
pip install -r requirements.txt


## Usage
ErrorDetector


Enter the input file name
Enter the desired name of the .txt report that will be generated 

## Output
Generates a `.txt` report with per-chunk analysis including:
- List or errors contextualised within the sentences
- List of correction of each error
- Fully corrected chunk

## How It Works
1. Reads the input `.txt` file
2. Splits the text into chunks of ~700 characters (~250-300 words)
3. Runs each chunk through the `gemma3:4b-it-qat` model with the following prompt:
   INSTRUCTION: Analyze the following academic text for English language errors. 
        Provide a structured report with the following sections:
        1. ERRORS: List all detected errors, numbered, with the original incorrect phrase quoted.
        2. SUGGESTED CORRECTIONS: For each error listed above, provide the corrected version.
        3. CORRECTED TEXT: The full original text rewritten with all corrections applied.
        4. ANALYSIS: Brief summary of the most frequent error types found. 
4. Writes a full report to the output `.txt` file

## Files Structure
- `ErrorDetector.py` - main program, run this to launch the app
- `CJAL.txt` - authentic paper where human and AI generated text is mixed (for testing)
- `reportCJAL.txt` - example of error detection report for the `CJAL.txt`
- `requirements.txt` — Python dependencies
- `README.md` — this file
- `app.py` - gradio interface

## Notes
- Chunk size is set to **700 characters** for optimal model performance
- Ollama must be running locally 