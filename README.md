# multi-agent-handwritten-notes
An autonomous multi-agent system built with LangGraph, Tavily, and Playwright that researches complex topics and renders handwritten-style student study notes into PNG screenshots.
# 🎓 Multi-Agent Handwritten Notes Generator

An autonomous multi-agent workflow built using **LangGraph**, **LangChain**, **Tavily Search**, and **Playwright**. The system researches complex technical concepts and dynamically compiles the findings into styled, handwritten-notebook PNG screenshots.

---

## 🏗️ System Architecture

[ User Input / Prompt ]
│
▼
[ Researcher Node ] ── (Tavily Web Search & Summarization)
│
▼
[ Note Renderer Node ] ── (HTML/CSS + Google Caveat Font + Playwright Screenshot)
│
▼
[ Critic Node ] ── (Validation Check: Is Output Complete?)
│
Approved? ──► No ──► [ Researcher Node ]
│
Yes
▼
[ PNG Screenshot Saved ]


## ⚡ Features

- **Autonomous Research:** Uses Tavily API to fetch up-to-date technical context.
- **Dynamic HTML/CSS Rendering:** Formats structured summaries into a paper-notebook layout utilizing Google's *Caveat* handwriting font.
- **Headless Browser Capture:** Captures high-resolution PNG screenshots via Playwright Chromium.
- **Stateful Loop Guards:** Implements LangGraph reflection loops with execution caps to prevent infinite credit consumption.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- OpenAI API Key
- Tavily Search API Key

### 2. Installation

Clone the repository and install dependencies:


# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements & Playwright browser
pip install -r requirements.txt
playwright install chromium

3. Environment Configuration

Copy the example environment file and add your credentials:
Bash

cp .env.example .env

Edit .env:
Code snippet

OPENAI_API_KEY="your_openai_api_key"
TAVILY_API_KEY="your_tavily_api_key"
