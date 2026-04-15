# GUI for Automatic Text Summarizer

import tkinter as tk
from tkinter import messagebox
import nltk
import re
import heapq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from tkinter import filedialog

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# -----------------------------------------
# Step 1: Read Input Text File
# -----------------------------------------
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# -----------------------------------------
# Step 2: Text Preprocessing
# -----------------------------------------
def preprocess_text(text):
    # Remove special characters
    clean_text = re.sub('[^a-zA-Z]', ' ', text)
    clean_text = clean_text.lower()
    
    # Tokenization
    words = word_tokenize(clean_text)
    sentences = sent_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    
    filtered_words = [word for word in words if word not in stop_words]
    
    return filtered_words, sentences

# -----------------------------------------
# Step 3: Calculate Word Frequency
# -----------------------------------------
def calculate_word_frequency(words):
    word_freq = {}
    
    for word in words:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1
    
    return word_freq

# -----------------------------------------
# Step 4: Normalize Frequency
# -----------------------------------------
def normalize_frequency(word_freq):
    max_freq = max(word_freq.values())
    
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq
    
    return word_freq

# -----------------------------------------
# Step 5: Score Sentences
# -----------------------------------------
def score_sentences(sentences, word_freq):
    sent_score = {}
    
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                if sent not in sent_score:
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]
    
    return sent_score

# -----------------------------------------
# Step 6: Generate Summary
# -----------------------------------------
def generate_summary(sent_score, num_sentences=3):
    summary_sentences = heapq.nlargest(num_sentences, sent_score, key=sent_score.get)
    return summary_sentences

# -----------------------------------------
# Step 7: Save Output
# -----------------------------------------
def save_summary(summary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for sentence in summary:
            file.write(sentence + "\n")

# -----------------------------------------
# Button Function
# -----------------------------------------
def summarize_text(text, num_sentences=3):
    words, sentences = preprocess_text(text)
    if not sentences:
        return "No sentences detected in the text. Please enter text with proper sentences."
    word_freq = calculate_word_frequency(words)
    if not word_freq:
        return "No words found after preprocessing. Please enter text with letters."
    word_freq = normalize_frequency(word_freq)
    sent_score = score_sentences(sentences, word_freq)
    if not sent_score:
        return "Unable to score sentences. Please enter longer text."
    summary_sentences = generate_summary(sent_score, min(num_sentences, len(sentences)))
    return '\n'.join(summary_sentences)

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        text = read_file(file_path)
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, text)

def generate_summary_button():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter text or upload a file.")
        return
    try:
        summary = summarize_text(input_text, 3)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, summary)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def clear_text():
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)

# -----------------------------------------
# GUI Design
# -----------------------------------------
root = tk.Tk()
root.title("Automatic Text Summarizer")
root.geometry("700x500")

# Title
label_title = tk.Label(root, text="Text Summarizer", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Input box
label_input = tk.Label(root, text="Enter Text:")
label_input.pack()

text_input = tk.Text(root, height=10, width=80)
text_input.pack(pady=5)
text_input.bind('<KeyRelease>', lambda e: generate_summary_button())

# Button
# Button Frame (to hold both buttons)
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Upload Button
btn_upload = tk.Button(frame_buttons, text="Upload File", command=upload_file)
btn_upload.pack(side=tk.LEFT, padx=10)

# Generate Button
btn_generate = tk.Button(frame_buttons, text="Generate Summary", command=generate_summary_button)
btn_generate.pack(side=tk.LEFT, padx=10)

# Clear Button
btn_clear = tk.Button(frame_buttons, text="Clear", command=clear_text)
btn_clear.pack(side=tk.LEFT, padx=10)

# Output box
label_output = tk.Label(root, text="Summary:")
label_output.pack()

text_output = tk.Text(root, height=10, width=80)
text_output.pack(pady=5)

# Run GUI
root.mainloop()