# SmartApply: Agno-Powered Job Application Agent

SmartApply is an AI-powered agent designed to automate and streamline the job application process for users. By leveraging Agno's powerful LLM capabilities, SmartApply helps users tailor and submit job applications faster, more accurately, and at scale.

---
## 🚀 How to run
1. comment down 4Mail.py it requires your Composio account API key
2. Place your resume (CV.pdf)
3. install requirements.txt, Optionally Change advanced models in 3Browser_ash.py like claude,.. if needed. and add environment variables openai, gemini, .. 
4. Run st_app.py ( JobsData.csv have list of jobs or you can also run app.py without ui )
5. Update preferences and click apply.


## 🚀 Features

- ✨ Resume Parsing and scoring
- ✉️ Personalized Cover Letter Generation
- 🔍 JD (Job Description) Matching and Keyword Highlighting like German, Spanish
- 🧠 Uses Agno LLM to contextualize and customize responses
- 📤 One-click Application Submission Flow (mocked/simulated)

---

## 🧠 Powered By

- **Agno agents**: Core engine for generating personalized, high-quality application content.
- **Browser Use**: Automation of job application.
- **V0**: User-friendly front-end upload JobsData.csv (https://v0-linkedin-like-portal.vercel.app/).
- **Composio**: sends email. 
---

## 📂 Project Structure

SmartApply/
├── app.py # Main app
├── UserData.py ( fill user preferences like salary,..)
├── 1JDa.py and 1JDb.py ( Scrapes latest jobs and save to JobsData.csv )
├── 1Score.py # Agno agents score resume against each job and checks for language requirement like German,..
├── 2CL.py # Automatically generates cover letter based on criteria (minimum match as 60%)
├── 3Browser_ash.py # Automatically fills job application 
├── 4Mail.py # Sends email to recruiter and user confirmation 
├── README.md # You're here!
├── CV.pdf ( Place your latest resume )
└── AddJob.py ( Place your job url and JD in JD.txt to add new job manually)




📸 Demo
https://youtu.be/dWA_qBwlwH8

Hi everyone! I'm excited to introduce SmartApply, an AI-powered job application agent built using Agno.

Applying to jobs can be repetitive and exhausting, especially when every job expects a custom resume and cover letter. SmartApply solves that.
First, just place your resume SmartApply will automatically match your resume with job descriptions, highlight important keywords like language requirements — say, German or Spanish — and even generate personalized cover letters using Agno’s powerful LLM.

It doesn’t stop there. With just one click, the agent can simulate applying to jobs, send confirmation emails using Composio, and even fill job forms automatically via browser automation.

There's also a simple front-end using V0, where you can upload job data and track everything.
SmartApply helps you go from resume to ready in seconds — personalized, automated, and scalable.
Check out the full demo and code, and thanks for watching!

