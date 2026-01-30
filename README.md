# AI-Study-Abroad-Counselor
AI Study Abroad Counselor is an AI-powered web application built to support students in making informed study abroad decisions. The platform provides a structured counseling workflow by combining university recommendations, shortlist management, SOP/resume feedback, an interactive AI chatbot, and downloadable reporting in a single system.
This project is designed to simulate the experience of a professional overseas education consultancy, enhanced with modern AI capabilities for personalized guidance.

## Live Application
The application is deployed publicly using Streamlit Cloud and can be accessed here:
https://ai-study-abroad-counselor.streamlit.app/

## Project Overview
This application helps students explore universities based on their academic profile and study preferences. It provides ranking-based recommendations, course-aware filtering, AI-driven counseling support, and structured documentation feedback.

The platform follows a guided student flow:
1. Student enters onboarding profile information  
2. Top universities are recommended based on course, ranking, and budget  
3. Universities can be shortlisted  
4. SOP/Resume can be reviewed using AI  
5. Students can chat with an AI counselor  
6. A final counseling report can be exported as a PDF  

## Key Features
### Student Profile Onboarding
The onboarding module collects important student information such as CGPA, target country, annual budget range, and intended course of study (e.g., AI, MBA, MS CS, Data Science). This profile is used throughout the application to ensure recommendations and counseling responses remain personalized.

### University Explorer and Matching
The University Explorer recommends the top 10 universities based on the student's intended course and selected country. Universities are sorted by global ranking and filtered intelligently to prioritize the student’s target program.

Each university card includes:
- Match percentage based on CGPA, tuition affordability, and scholarship chance  
- City and global ranking  
- Tuition fee and scholarship category  
- Programs offered  
- Official university website link  

Shortlisting is supported directly within the explorer interface.

### University Shortlisting
Students can shortlist universities from the recommendation list. The shortlisted universities remain visible in the session, allowing students to track preferred options during counseling and reporting.

### SOP and Resume Feedback
The SOP/Resume Review module accepts PDF or text uploads and generates structured AI feedback. The system does not repeat the document content, but instead provides improvement-focused analysis in the following format:
1. Key strengths  
2. Weaknesses and missing areas  
3. Improvement suggestions  
4. Rewrite recommendations  
This helps students enhance the quality, clarity, and competitiveness of their applications.

### AI Chatbot Counseling
The platform includes a conversational chatbot that provides responses similar to ChatGPT. The chatbot automatically uses:
- The student onboarding profile  
- The shortlisted universities  
- The current user query  
This ensures context-aware and personalized counseling support for university selection, scholarships, admissions planning, and course guidance.

### Exportable Counseling Report
A complete counseling report can be downloaded in PDF format. The report includes:
- Student profile summary  
- SOP/Resume feedback output  
- Full chatbot conversation history  
This makes the counseling results portable and useful for future reference.

## Technology Stack
The project uses modern AI and deployment tools:
- Streamlit for frontend development and deployment  
- Groq API (LLaMA 3.1) for chatbot and feedback generation  
- Pandas for dataset filtering and university matching  
- PyPDF for extracting SOP/Resume text  
- FPDF for PDF report generation  
- streamlit-antd-components for sidebar navigation and UI enhancement  

## Running the Project Locally
Follow these steps to run the application on your system.

1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-study-abroad-counselor.git
cd ai-study-abroad-counselor

2. Install Dependencies
```bash
pip install -r requirements.txt

3. Configure the Groq API Key
Create a secrets file at:
```bash
.streamlit/secrets.toml

Add your Groq API key:
```bash
GROQ_API_KEY="your_api_key_here"

4. Run the Application
```bash
streamlit run ai_counselor_app/app.py


**Deployment**

The application is deployed using Streamlit Community Cloud. Deployment involves:
- Uploading the project to GitHub
- Connecting the repository to Streamlit Cloud
- Adding the Groq API key securely using Streamlit Secrets
- Launching the app publicly

Future Enhancements

Planned improvements include:
- University comparison dashboard for shortlisted options
- Integration of real QS/THE ranking datasets
- Scholarship prediction using ML models
- Browser-based voice assistant support
- More advanced program and location filters

