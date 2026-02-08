Add Professional README.md (English)
Goal Description
Create a professional, high-quality README.md in English for the food-scun project. The document will highlight the project's capabilities (AI-powered food analysis), modern architecture, and stack.


Proposed Changes
Root Directory
[NEW] 
README.md
Header: Project Title, Short Description, Badges (Python, Django, Poetry, License).
About: Detailed description of the project's purpose - scanning food and getting health insights using Google Gemini.
Key Features:
🤖 AI-Powered Analysis: Detailed breakdown of ingredients and health scores using Google Gemini Pro/Flash.
🍎 Smart Scoring: Automatic health scoring (0-100) and summary generation.
🔐 Secure Authentication: OAuth 2.0 support for Google and Apple sign-in.
🏗 Clean Architecture: Separation of concerns with dedicated services for AI and Auth logic.
Tech Stack:
Backend: Django 5+, Django Rest Framework (DRF).
AI: Google Generative AI (Gemini).
Database: PostgreSQL.
Dependency Management: Poetry.
Authentication: JWT, social-auth-app-django (implied or custom via external_api).
Getting Started:
Prerequisites: Python 3.11+, Poetry.
Installation: Step-by-step guide (git clone, poetry install).
Configuration: 
.env
 file setup (GEMINI_API_KEY, DB credentials).
Running the App: python manage.py runserver.
Project Structure: Brief tree view highlighting apps/food and apps/user.
Verification Plan
Manual Verification
Review the generated README.md for tone, grammar, and formatting.
Verify that generic badges/links are replaced with placeholders or correct info.
