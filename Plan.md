# Manim Paper Agent - Project Plan

## Project Overview
Build an AI agent system that reads scientific papers (PDFs) and automatically generates Manim animations explaining key mathematical concepts.

## Tech Stack
- **LLM**: Google Gemini API (2.0 Flash + 1.5 Pro)
- **Animation**: Manim Community Edition
- **Language**: Python 3.10+
- **Architecture**: Multi-agent system (no framework)

---

## Phase 1: MVP (Week 1) - Core Pipeline

### Day 1-2: Foundation
**Goal**: Get PDF → Concepts extraction working

**Tasks**:
- [ ] Set up project structure
- [ ] Configure Gemini API
- [ ] Implement `analyzer.py` agent
  - Upload PDF to Gemini
  - Extract 3-5 mathematical concepts
  - Output structured JSON
- [ ] Test with 3 sample papers

**Success Criteria**:
- Can extract concepts from any math/ML paper
- JSON output is clean and structured
- Concepts are actually visualizable

**Files to create**:
- `agents/analyzer.py`
- `utils/pdf_handler.py`
- `prompts/analyzer_prompt.py`
- `config.py`

---

### Day 3-4: Code Generation
**Goal**: Concepts → Working Manim scripts

**Tasks**:
- [ ] Implement `generator.py` agent
- [ ] Create library of 10+ Manim example scripts
- [ ] Build prompt with examples and best practices
- [ ] Test generation on extracted concepts
- [ ] Implement code cleaning (remove markdown, etc.)

**Success Criteria**:
- Generates syntactically valid Python
- Uses proper Manim imports and structure
- At least 60% of scripts run without errors

**Files to create**:
- `agents/generator.py`
- `prompts/generator_prompt.py`
- `examples/manim_examples.py`
- `utils/code_cleaner.py`

---

### Day 5: Validation & Execution
**Goal**: Validate scripts and render videos

**Tasks**:
- [ ] Implement