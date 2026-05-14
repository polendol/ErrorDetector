# Error Detector

## Description
This error detector uses Gemma model to detect English errors in writing of any .txt file within the project and 
generates report (.txt file) by chunks listing errors and corrections. As academic papers in preparation are privacy-sensitive, 
this program has been created to facilitate error detection during text editing without submitting the documents online
for error detection prior to publication. This model is run locally through Ollama and requires pulling `gemma3:4b-it-qat`.

The text is analysed by chunks of 700 characters (100 words), to imitate the
average paragraph size of the text.

The input files must be .txt files. Report is generated as .txt file within the same project. 

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

## Notes
- Chunk size is set to **700 characters** for optimal model performance
- Ollama must be running locally 