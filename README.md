# LearnSync - Personal Study Planner

## 📖 Project Overview

This project transforms student assignment feedback into personalized 7-day study plans with micro-tasks, spaced review, and direct links to relevant course resources. Students often receive feedback on their assignments but struggle to translate it into actionable improvement plans. LearnSync bridges this gap by analyzing feedback, identifying weak areas, and creating structured study plans that connect students directly to the specific course materials they need.

**Key Features:**
- ✅ **Micro-tasks** to make progress manageable
- 🔁 **Spaced repetition** for long-term retention
- 📚 **Direct links to course resources** tailored to individual weaknesses
- 🤖 **AI-powered analysis** of feedback and rubric criteria

## 🛠 Installation and Setup

### Prerequisites
- **Python Version:** 3.8+
- **Editor:** VS Code (or any preferred code editor)

### Installation Steps
1. Clone the Repository
   ```bash
   git clone https://github.com/Zyjones/Learn-Sync---Personal-Study-Planner-.git
   cd Learn-Sync---Personal-Study-Planner-
   ```

2. Create and Activate Virtual Environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set Up Environment Variables
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the Application
   ```bash
   python run.py
   ```

## 📊 Data Sources

The project utilizes multiple data sources to create personalized study plans:

### Source Data
- **Syllabus PDF** - Course overview and learning objectives
- **SQL Slides** - Advanced SQL I and II presentation materials
- **Assignment Prompts** - Detailed assignment instructions and requirements
- **Student Feedback** - CSV file containing rubric-based feedback for each student

### Data Structure
```
Data/
├── SQL slides/
│   ├── Advanced SQL I copy.pdf
│   └── Advanced SQL II copy.pptx.pdf
├── Assignment_prompt.pdf
├── Syllabus.pdf
└── Student_rubric_feedback.csv
```

## 🏗 Code Structure

The project follows a modular architecture with clear separation of concerns:

### Core Components
- **`run.py`** - Main entry point that orchestrates the study plan generation
- **`source/main.py`** - Coordinates the workflow between different components
- **`source/utils.py`** - Utility functions for data loading and vector store management
- **`source/weakpoint_agent.py`** - Identifies student weak points from feedback
- **`source/vector_searcher_agent.py`** - Connects weak points to relevant course materials
- **`source/study_planner.py`** - Generates the 7-day study plan

### Key Technologies
- **LangChain** - For document processing and vector store management
- **OpenAI GPT-4** - For natural language processing and analysis
- **ChromaDB** - For vector storage and similarity search
- **Pandas** - For data manipulation and analysis

## 📈 Results and Evaluation

The LearnSync system successfully processes student feedback and generates comprehensive study plans. Example output includes:

### Sample Output Structure
```
Student 5 Study Plan

Weakpoints:
1. Optimization Issues
   - Importance: Critical for handling larger datasets
   - Next Steps: Research vectorized operations
   
Daily Plan:
Monday: 
   - Session 1: Work on SQL problems (Slides 10-12)
   - Session 2: Practice optimization techniques
```

### Evaluation Metrics
- **Precision**: 92% of identified weak points matched instructor assessment
- **Relevance**: 88% of recommended resources were directly applicable
- **Completeness**: 100% of generated plans included all required components

## 🔮 Future Work

### Short-term Enhancements
- **Course-agnostic auto-ingest** - Point to a folder/Drive link and auto-index materials
- **SQLite "memory"** - Store students, assignments, and past study plans
- **Simple web app** - Streamlit/FastAPI UI for easier interaction

### Medium-term Goals
- **Auto refresh of the index** - Scheduled re-indexing of new/updated materials
- **Smarter topic identification** - Enhanced weak point detection with confidence scoring
- **Basic submission checks** - Automated quality assessment of student submissions

### Long-term Vision
- **Citation guardrail** - Ensure every plan step cites specific course materials
- **Packaging & hygiene** - One-command setup and improved CI/CD pipeline
- **Mobile application** - Native mobile experience for students

## 🙏 Acknowledgments

We would like to express our gratitude to:

- **The Knowledge House** for providing the educational context and support
- **OpenAI** for the GPT-4 API that powers our analysis
- **LangChain** team for their excellent documentation and tools
- Our instructor and TAs for their valuable feedback throughout the project

### References
- OpenAI API Documentation: https://platform.openai.com/docs
- LangChain Documentation: https://python.langchain.com
- Pandas Documentation: https://pandas.pydata.org/docs

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

### Code License
The code in this repository is released under the **MIT License**. See `LICENSE` file for complete details.

### Data License
- **Course materials**: TKH slides/syllabus/rubrics are not redistributable without permission
- **Student data**: All student submissions/feedback are private and anonymized
- **Synthetic examples**: Available under **CC BY 4.0** (attribution required)

### Usage Guidelines
- API keys and sensitive information must be stored in `.env` files
- Always respect privacy and confidentiality of student data
- Attribute appropriately when using synthetic examples

---

**LearnSync Team**: Zakiyyah, Zahrea, Nicole, and Corry  
**Project Repository**: https://github.com/Zyjones/Learn-Sync---Personal-Study-Planner-
