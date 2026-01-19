#!/usr/bin/env python3
"""
PDF Reader that uses the main Jarvis TTS engine - No threading conflicts
"""

import PyPDF2
import os
import time
from pathlib import Path

class PDFReaderNoTTS:
    def __init__(self):
        self.current_pdf = None
        self.is_reading = False
        self.stop_reading_flag = False
        self.current_text = ""
        self.current_sentences = []
        self.current_sentence_index = 0
        
    def find_pdf_file(self, filename):
        """Find PDF file in current directory or pdf folder"""
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        search_paths = [
            filename,
            os.path.join("pdf", filename),
            os.path.join("pdfs", filename),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        return None
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using PyPDF2"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            return f"Error extracting text: {e}"
    
    def clean_text_for_speech(self, text):
        """Clean text for better speech synthesis"""
        import re
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', ' ', text)
        text = text.replace('�', ' ')
        text = text.replace('\x00', ' ')
        return text.strip()
    
    def prepare_pdf_for_reading(self, pdf_path, max_length=3000):
        """Prepare PDF text for reading - returns sentences to be read"""
        try:
            # Find PDF file
            if not os.path.exists(pdf_path):
                found_path = self.find_pdf_file(pdf_path)
                if found_path:
                    pdf_path = found_path
                else:
                    return None, f"PDF file '{pdf_path}' not found"
            
            # Extract and clean text
            text = self.extract_text_from_pdf(pdf_path)
            if text.startswith("Error"):
                return None, text
            
            clean_text = self.clean_text_for_speech(text)
            if not clean_text:
                return None, "No readable text found in PDF"
            
            # Limit text length
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "... Text truncated for reading."
            
            # Split into sentences
            sentences = clean_text.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Store reading state
            self.current_pdf = pdf_path
            self.current_text = clean_text
            self.current_sentences = sentences
            self.current_sentence_index = 0
            self.is_reading = True
            self.stop_reading_flag = False
            
            return sentences, f"Prepared {len(sentences)} sentences for reading"
            
        except Exception as e:
            return None, f"Error preparing PDF: {e}"
    
    def get_next_sentence(self):
        """Get the next sentence to read"""
        if not self.is_reading or self.stop_reading_flag:
            return None
        
        if self.current_sentence_index < len(self.current_sentences):
            sentence = self.current_sentences[self.current_sentence_index]
            self.current_sentence_index += 1
            return sentence
        else:
            # Finished reading
            self.is_reading = False
            return None
    
    def stop_reading(self):
        """Stop current reading"""
        if self.is_reading:
            self.stop_reading_flag = True
            self.is_reading = False
            sentences_read = self.current_sentence_index
            total_sentences = len(self.current_sentences)
            return f"PDF reading stopped after {sentences_read} of {total_sentences} sentences"
        else:
            return "No PDF is currently being read"
    
    def get_reading_status(self):
        """Get current reading status"""
        if self.is_reading:
            pdf_name = os.path.basename(self.current_pdf) if self.current_pdf else "Unknown PDF"
            progress = f"{self.current_sentence_index}/{len(self.current_sentences)}"
            return f"Reading: {pdf_name} - Progress: {progress} sentences"
        else:
            return "No PDF is currently being read"
    
    def get_reading_progress(self):
        """Get reading progress as percentage"""
        if self.is_reading and self.current_sentences:
            return (self.current_sentence_index / len(self.current_sentences)) * 100
        return 0
    
    def list_pdfs(self):
        """List available PDF files"""
        try:
            pdf_files = []
            
            # Check current directory
            for file in os.listdir("."):
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file)
            
            # Check pdf folder
            if os.path.exists("pdf"):
                for file in os.listdir("pdf"):
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(f"pdf/{file}")
            
            if not pdf_files:
                return "No PDF files found"
            
            return f"Found {len(pdf_files)} PDF files: " + ", ".join(pdf_files)
            
        except Exception as e:
            return f"Error listing PDFs: {e}"

# Global instance
pdf_reader_no_tts = PDFReaderNoTTS()

# Convenience functions
def prepare_pdf_reading(filename):
    """Prepare PDF for reading - returns sentences list"""
    return pdf_reader_no_tts.prepare_pdf_for_reading(filename)

def get_next_pdf_sentence():
    """Get next sentence to read"""
    return pdf_reader_no_tts.get_next_sentence()

def stop_pdf_reading():
    """Stop PDF reading"""
    return pdf_reader_no_tts.stop_reading()

def get_pdf_reading_status():
    """Get PDF reading status"""
    return pdf_reader_no_tts.get_reading_status()

def is_pdf_reading():
    """Check if PDF is being read"""
    return pdf_reader_no_tts.is_reading

def get_pdf_progress():
    """Get reading progress percentage"""
    return pdf_reader_no_tts.get_reading_progress()

def list_available_pdfs():
    """List available PDFs"""
    return pdf_reader_no_tts.list_pdfs()