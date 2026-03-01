from fpdf import FPDF
import os

class DocumentEngine:
    def __init__(self):
        pass

    def create_pdf(self, content, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Professional font - Arial is standard
        pdf.set_font("Arial", size=11)
        
        # Split content by lines
        for line in content.split('\n'):
            # Skip empty lines but add spacing
            if not line.strip():
                pdf.ln(4)
                continue

            # 1. Strip Markdown formatting for PDF readability
            # Remove header symbols and trim
            text = line.lstrip('#').strip()
            # Remove bold/italic symbols
            text = text.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
            
            # 2. Basic character cleanup for PDF compatibility
            text = text.replace('•', '-').replace('–', '-').replace('—', '-').replace('’', "'").replace('“', '"').replace('”', '"')
            
            # 3. Apply formatting based on original line structure
            if line.strip().startswith('#'):
                pdf.set_font("Arial", 'B', size=14)
                pdf.set_text_color(0, 0, 0) # Force black
                h = 10
            else:
                pdf.set_font("Arial", size=11)
                pdf.set_text_color(51, 51, 51) # Dark gray for body
                h = 7

            # 4. Explicitly set X to margin and use left alignment to fix "pushed to right" issue
            pdf.set_x(pdf.l_margin)
            try:
                # Use align='L' to be absolutely sure
                pdf.multi_cell(w=pdf.epw, h=h, txt=text.encode('latin-1', 'replace').decode('latin-1'), align='L')
            except Exception:
                # Absolute fallback for complex lines
                words = text.split(' ')
                for word in words:
                    if pdf.get_string_width(word) > (pdf.epw - 5):
                        word = word[:25] + "..."
                    pdf.write(h, word.encode('latin-1', 'replace').decode('latin-1') + " ")
                pdf.ln(h)
            
        # Ensure data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        output_path = os.path.join("data", filename)
        pdf.output(output_path)
        return output_path

    def create_html_portfolio(self, user_data, sections):
        # Modern Dark-themed HTML template
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{user_data.get('name', 'My Portfolio')}</title>
            <style>
                :root {{ --primary: #6366F1; --bg: #0F172A; --card: #1E293B; --text: #F8FAFC; }}
                body {{ font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; color: var(--text); background-color: var(--bg); max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
                header {{ text-align: center; margin-bottom: 50px; padding: 40px; background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
                h1 {{ font-size: 2.5rem; margin: 0; }}
                header p {{ opacity: 0.9; font-size: 1.1rem; }}
                section {{ background: var(--card); padding: 30px; margin-bottom: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }}
                h2 {{ color: var(--primary); font-size: 1.5rem; margin-top: 0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }}
                .skills {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 15px; }}
                .skill-tag {{ background: rgba(99, 102, 241, 0.2); color: #818CF8; padding: 6px 15px; border-radius: 10px; font-size: 0.9rem; font-weight: 600; border: 1px solid rgba(99, 102, 241, 0.3); }}
                .exp-content {{ white-space: pre-wrap; color: #CBD5E1; }}
            </style>
        </head>
        <body>
            <header>
                <h1>{user_data.get('name', 'Your Name')}</h1>
                <p>{user_data.get('email', '')} {'| ' + user_data.get('phone', '') if user_data.get('phone') else ''}</p>
            </header>
            
            <section>
                <h2>About Me</h2>
                <p>{sections.get('summary', 'Passionate professional looking for new opportunities.')}</p>
            </section>
            
            <section>
                <h2>Technical Expertise</h2>
                <div class="skills">
                    { "".join([f'<span class="skill-tag">{s.strip()}</span>' for s in user_data.get('skills', '').split(',') if s.strip()]) }
                </div>
            </section>

            <section>
                <h2>Work & Projects</h2>
                <div class="exp-content">{sections.get('experience', 'Available upon request.')}</div>
            </section>
        </body>
        </html>
        """
        output_path = os.path.join("data", "portfolio.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return output_path
