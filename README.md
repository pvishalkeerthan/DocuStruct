<div align="center">

# 📄 DocuStruct

### *Intelligent PDF Document Structure Analyzer*

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org)
[![PDF](https://img.shields.io/badge/PDF-Processing-red?logo=adobe)](https://en.wikipedia.org/wiki/PDF)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## Overview

DocuStruct is an intelligent PDF document structure analyzer that extracts hierarchical headings from PDF files using advanced font size detection and color analysis. It automatically identifies document titles and creates structured outlines with precision and elegance.

## Features

- **Smart Heading Detection**: Automatically identifies H1, H2, H3 levels based on font size frequency analysis
- **Color-Aware Extraction**: Detects and preserves text colors for better document structure understanding
- **Title Extraction**: Automatically detects document titles from the first page using bold text heuristics
- **Structured JSON Output**: Generates clean, hierarchical document outlines
- **Docker Ready**: Fully containerized for consistent cross-platform execution
- **Batch Processing**: Process multiple PDFs simultaneously
- **Robust Error Handling**: Continues processing even when individual pages fail

## Quick Start

### Prerequisites

- Docker installed on your system

### Installation & Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pvishalkeerthan/DocuStruct.git
   cd DocuStruct
   ```

2. **Build Docker Image**
   ```bash
   docker build --platform=linux/amd64 -t docustruct:latest .
   ```

3. **Prepare Your PDFs**
   ```bash
   # Create input directory and add your PDFs
   mkdir -p input
   cp /path/to/your/documents/*.pdf input/
   ```

4. **Run DocuStruct**

   **Linux/macOS:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     docustruct:latest
   ```

   **Windows PowerShell:**
   ```powershell
   docker run --rm `
     -v ${PWD}/input:/app/input `
     -v ${PWD}/output:/app/output `
     docustruct:latest
   ```

   **Windows Command Prompt:**
   ```cmd
   docker run --rm ^
    -v %cd%\input:/app/input ^
    -v %cd%\output:/app/output ^
    docustruct:latest

   ```

## Project Structure

```
DocuStruct/
├── Dockerfile              # Container configuration
├── main.py                 # Core PDF processing logic
├── requirements.txt        # Python dependencies (pdfplumber==0.10.2)
├── input/                  # PDF input directory
│   ├── document1.pdf
│   ├── research_paper.pdf
│   └── technical_manual.pdf
├── output/                 # JSON output directory
│   ├── document1.json
│   ├── research_paper.json
│   └── technical_manual.json
└── README.md              # This file
```

## Output Format

DocuStruct generates structured JSON files with document titles and hierarchical outlines:

```json
{
  "title": "Machine Learning Fundamentals: A Comprehensive Guide",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction to Machine Learning",
      "color": "black",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Supervised Learning Algorithms",
      "color": "blue",
      "page": 3
    },
    {
      "level": "H3",
      "text": "Linear Regression Analysis",
      "color": "black",
      "page": 5
    },
    {
      "level": "H2",
      "text": "Neural Networks Overview",
      "color": "red",
      "page": 8
    }
  ]
}
```

### Output Schema Details

| Field | Description |
|-------|-------------|
| `title` | Document title extracted from first page (bold text or longest line) |
| `outline` | Array of detected headings |
| `level` | Heading hierarchy: H1 (largest), H2 (medium), H3 (smallest) |
| `text` | Heading text content |
| `color` | Text color: black, red, blue, green, yellow, white, or rgb(r,g,b) |
| `page` | Page number where heading appears |

## How It Works

### 1. Font Size Analysis
- Collects all font sizes across the document
- Identifies the 5 most common font sizes
- Maps largest sizes to heading levels (H1 > H2 > H3)

### 2. Color Detection
- Extracts RGB values from PDF text objects
- Maps colors to human-readable names
- Preserves color information for structural analysis

### 3. Title Extraction
- Prioritizes bold text from the first page
- Falls back to the longest text line in top 5 lines
- Handles edge cases with missing or malformed titles

### 4. Text Grouping
- Groups words by vertical position (y-coordinate)
- Sorts words horizontally within each line
- Applies appropriate spacing rules
- Preserves original text formatting

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pdfplumber | 0.10.2 | PDF text extraction and font analysis |
| unicodedata | Built-in | Character detection and normalization |
| collections | Built-in | Font frequency analysis |
| json | Built-in | Output formatting |
| logging | Built-in | Process monitoring and debugging |

## Algorithm Details

### Font Size Detection
- **Collection Phase**: Extracts font sizes from all text elements
- **Frequency Analysis**: Uses Counter to find most common sizes
- **Hierarchy Mapping**: Assigns H1/H2/H3 based on size ranking
- **Threshold Filtering**: Removes outliers and noise

### Color Processing
- Converts PDF color space to RGB
- Handles grayscale and CMYK color models
- Maps similar colors to standard names
- Preserves exact RGB for unique colors

### Text Processing
- Groups words by vertical position and font size
- Maintains proper text ordering within lines
- Handles special characters and formatting
- Preserves document structure integrity

## Performance

| PDF Type | Pages | Processing Time | Memory Usage |
|----------|-------|----------------|--------------|
| Text-only | 1-50 | < 5s | ~100MB |
| Mixed content | 50-200 | 5-15s | ~200MB |
| Complex layouts | 200+ | 15-30s | ~300MB |

## Acknowledgments

- Built with [pdfplumber](https://github.com/jsvine/pdfplumber) for robust PDF text extraction
- Color detection algorithms adapted from computer vision techniques

---
