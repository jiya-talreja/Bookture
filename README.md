

# Bookture

Bookture is an AI-powered visual storytelling platform that converts page-wise book text into contextual visual scenes. It generates illustrations for individual pages on demand while preserving narrative continuity and page-level meaning.

The system is designed for student literature and English curriculum enhancement — where textual learning often lacks visual representation — and for fiction readers who want to experience stories beyond imagination.

---

## Vision

Traditional literature education relies heavily on text. While this strengthens reading ability, it often limits visual comprehension, especially for complex scenes.

Bookture transforms static reading into an interactive visual experience by:

* Preserving page context
* Maintaining narrative integrity
* Generating AI-powered illustrations per page
* Enabling structured text-to-image experimentation

---

## Core Features

* Page-wise text processing
* On-demand image generation
* Context-aware prompt creation
* Literature-focused AI visualization
* Clean frontend interface for selective page rendering

---

## Intelligent PDF Ingestion Pipeline

Bookture includes a structured ingestion pipeline before any generation occurs.

### 1. File Validation Layer

* Accepts only PDF files
* Explicit rejection logic for non-PDF formats
* Prevents unsupported uploads

### 2. PDF Classification

The system classifies uploaded PDFs into:

* Text-based PDFs
* Scanned PDFs

The current implementation supports text-based PDFs.

Scanned PDFs are detected and rejected to maintain reliable NLP extraction quality and avoid inconsistent prompt generation.

---

### 3. TOC-Based Chapter Extraction Logic

To preserve story structure and narrative integrity:

* The system analyzes the Table of Contents (TOC)
* Automatically detects the starting page of Chapter 1
* Ignores front matter such as forewords, publisher notes, indexes, and metadata
* Begins processing only from the actual story content

This ensures that generated visuals correspond strictly to narrative content.

---

### 4. Header and Footer Removal

To improve text cleanliness and prompt precision:

* Repeated headers are detected and removed
* Repeated footers are removed
* Page numbers and formatting artifacts are cleaned

This prevents structural noise from influencing NLP processing and image prompt construction.

---

## AI and Generation Pipeline

1. Cleaned page text is processed using NLP logic.
2. Context-aware prompts are constructed per page.
3. Prompts are sent to the image generation model.
4. Generated images are returned and mapped to their corresponding pages.

Image model used:

* pixazo.ai/flux-2-klein-4b

The system focuses on structured and controllable text-to-image transformation rather than generic generation.

---

## Tech Stack

Frontend

* React (TypeScript / TSX)
* Simple CSS

Backend

* Python
* FastAPI

AI Layer

* NLP-based prompt construction
* pixazo.ai/flux-2-klein-4b image generation model

---

## System Architecture (High-Level Flow)

User uploads PDF
↓
PDF validation
↓
PDF classification (Text vs Scanned)
↓
TOC analysis → Chapter 1 detection
↓
Header and footer cleaning
↓
Page-wise text segmentation
↓
Prompt engineering
↓
Image generation
↓
Frontend rendering

---

## Target Audience

* Students studying literature or English curriculum
* Teachers seeking visual teaching aids
* Fiction book readers
* AI and NLP experimentation projects
* Text-to-image research workflows

---

## Current Scope

* Supports only text-based PDFs
* Page-level image generation
* Manual on-demand rendering per page
* Structured ingestion and preprocessing pipeline

---

## Future Enhancements

* OCR support for scanned PDFs
* Multi-page contextual memory
* Character consistency modeling
* Style selection system
* Image caching and generation history
* Deployment and scaling infrastructure

---

## Getting Started

Backend:

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend:

cd frontend
npm install
npm run dev

---

## Project Philosophy

Bookture does not aim to replace reading.

It aims to enhance understanding.

By merging literature with AI-generated visuals, it introduces an interactive layer to traditional storytelling while preserving the integrity and structure of the original text.
