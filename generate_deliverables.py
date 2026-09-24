from fpdf import FPDF

class DeliverablesPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Code Sentry - Assignment Deliverables", align="C")
        self.ln(20)

    def section(self, title, body, link=""):
        self.set_font("Arial", "B", 13)
        self.cell(0, 8, title, ln=True)
        
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 7, body)
        
        if link:
            self.set_text_color(0, 0, 255)
            self.set_font("Arial", "U", 12)
            self.cell(0, 7, link, link=link, ln=True)
            self.set_text_color(0, 0, 0) # Reset color
            self.set_font("Arial", "", 12)
        
        self.ln(10)

pdf = DeliverablesPDF()
pdf.add_page()

# Section 1
title1 = "1. Source code in a repository (GitHub or zipped folder)"
body1 = "The complete source code for the AI-powered security reviewer (Code Sentry) has been organized into a dedicated project directory and successfully pushed to a public GitHub repository. You can access all project files at the following link:"
link1 = "https://github.com/ayushkale06/code-sentry"
pdf.section(title1, body1, link1)

# Section 2
title2 = "2. README.md"
body2 = "A comprehensive README.md file is included at the root of the repository. It successfully covers the required setup instructions (including the 'google-genai' dependency and API keys), instructions on how to run both the main application and the unit tests, a complete example of input and output, and the assumptions made regarding model routing and SDK error handling."
pdf.section(title2, body2)

# Section 3
title3 = "3. A short demo"
body3 = "A fully self-contained demo is implemented within 'main.py'. By running the script directly, it automatically provides a sample vulnerable Python snippet (containing OS command injection and weak MD5 hashing) and a natural language query to the AI agent. The resulting structured output is clearly printed to the terminal. The exact code snippet and resulting output are also permanently documented within the README.md file."
pdf.section(title3, body3)

pdf.output("Assignment_Deliverables.pdf")
print("Deliverables PDF generated successfully.")
