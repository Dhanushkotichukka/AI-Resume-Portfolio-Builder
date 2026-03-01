import google.generativeai as genai
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMHandler:
    def __init__(self, provider="Gemini", api_key=None, model_name=None):
        self.provider = provider
        self.api_key = api_key or (os.getenv("GOOGLE_API_KEY") if provider == "Gemini" else os.getenv("GROQ_API_KEY"))
        self.model_name = model_name
        
        self.gemini_model = None
        self.groq_client = None
        if self.provider == "Gemini":
            if self.api_key:
                genai.configure(api_key=self.api_key)
                # We will initialize the model in generate_content to allow fallbacks
        elif self.provider == "Groq":
            if self.api_key:
                self.groq_client = Groq(api_key=self.api_key)

    def generate_content(self, prompt):
        if self.provider == "Gemini":
            if not self.api_key:
                return "Gemini API Key not configured."
            
            # List of models found to be supported for this API key
            models_to_try = []
            if self.model_name:
                models_to_try.append(self.model_name)
            
            # Use the verified models found in the list_models check
            verified_models = [
                'models/gemini-2.0-flash', 
                'models/gemini-2.0-flash-lite', 
                'models/gemini-flash-latest',
                'models/gemini-pro-latest',
                'models/gemini-1.5-flash', # Fallback just in case
                'gemini-1.5-flash'
            ]
            
            for m in verified_models:
                if m not in models_to_try:
                    models_to_try.append(m)
            
            last_err = ""
            for m in models_to_try:
                try:
                    model = genai.GenerativeModel(m)
                    response = model.generate_content(prompt)
                    return response.text
                except Exception as e:
                    last_err = str(e)
                    # Try next if it's a 404 or support error
                    if "404" in last_err or "not found" in last_err.lower() or "not supported" in last_err.lower():
                        continue
                    break
            
            return f"Gemini Error (Tried multiple models): {last_err}. Tip: Try switching to 'Groq' in the sidebar or check your API key."
        
        elif self.provider == "Groq":
            if not self.groq_client:
                return "Groq API Key not configured."
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                return f"Groq Error: {str(e)}"
        
        return "Invalid Provider selected."

    def generate_resume_sections(self, user_data, target_role):
        prompt = f"""
        Generate a professional resume for a {target_role} position based on the following user details:
        {user_data}
        
        Please structure the output into the following sections:
        1. Professional Summary (Compelling and ATS-friendly)
        2. Key Skills (Relevant to {target_role})
        3. Experience/Projects (Quantifiable achievements)
        4. Education (Summarized)
        
        Use a professional tone and include relevant keywords for ATS optimization.
        Return the result in clear markdown formatting.
        """
        return self.generate_content(prompt)

    def generate_cover_letter(self, user_data, target_role, company_name="the company"):
        prompt = f"""
        Write a professional cover letter for a {target_role} position at {company_name}.
        User Details: {user_data}
        
        The letter should be persuasive, highlight relevant skills, and follow a standard professional format.
        Return the result in clear markdown formatting.
        """
        return self.generate_content(prompt)

    def optimize_keywords(self, current_resume, job_description):
        prompt = f"""
        Compare the following resume with the job description and suggest 5-10 missing keywords or phrases to improve ATS ranking.
        
        Resume:
        {current_resume}
        
        Job Description:
        {job_description}
        
        Provide the suggestions as a bulleted list with brief explanations why they are important.
        """
        return self.generate_content(prompt)
