import os

def create_sample_pdf_with_text():
    """
    Creates a sample PDF with text content for testing.
    Uses reportlab if available, otherwise provides instructions.
    """
    if not os.path.exists("files"):
        os.makedirs("files")
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        pdf_path = "files/sample_policy.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Add title and content
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Company Leave Policy - 2026")
        
        c.setFont("Helvetica", 12)
        y_position = 700
        
        content = [
            "Introduction:",
            "This document outlines our company's leave policy for all employees.",
            "",
            "Annual Leave:",
            "All full-time employees are entitled to 20 days of paid annual leave per year.",
            "Leave requests must be submitted at least 2 weeks in advance.",
            "",
            "Sick Leave:",
            "Employees receive 10 days of paid sick leave annually.",
            "A medical certificate is required for absences exceeding 3 consecutive days.",
            "",
            "Personal Leave:",
            "Employees may request up to 5 days of unpaid personal leave per year.",
            "Personal leave is subject to manager approval.",
            "",
            "Public Holidays:",
            "All employees are entitled to paid public holidays as per the national calendar.",
            "",
            "Contact:",
            "For questions about leave policies, contact HR at hr@company.com"
        ]
        
        for line in content:
            c.drawString(100, y_position, line)
            y_position -= 20
        
        c.save()
        print(f"✅ Created sample PDF with text content: {pdf_path}")
        return True
        
    except ImportError:
        print("⚠️ reportlab not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        print("✅ reportlab installed. Please run this script again.")
        return False

if __name__ == "__main__":
    create_sample_pdf_with_text()
