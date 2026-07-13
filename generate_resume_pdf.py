import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    # 1. Parse index.html
    if not os.path.exists("index.html"):
        print("Error: index.html not found.")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Clean up HTML comments
    html_clean = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    # Extract name & role
    name = "Hardik Khandhar"
    role = "Senior Full Stack Developer"
    name_match = re.search(r'class="profile-name">([^<]+)</h3>', html_clean)
    if name_match:
        name = name_match.group(1).strip()
    role_match = re.search(r'class="profile-role">([^<]+)</p>', html_clean)
    if role_match:
        role = role_match.group(1).strip()

    # Extract contact info
    location = "Ahmedabad, Gujarat, India"
    email = "hardikkhandhar100@gmail.com"
    phone = "+917878981685"

    loc_match = re.search(r'Location</span>\s*<span class="detail-value">([^<]+)</span>', html_clean)
    if loc_match:
        location = loc_match.group(1).strip()

    email_match = re.search(r'Email</span>\s*<span class="detail-value"><a href="mailto:([^"]+)"', html_clean)
    if email_match:
        email = email_match.group(1).strip()

    phone_match = re.search(r'Phone & WhatsApp</span>\s*<span class="detail-value"><a href="tel:([^"]+)"', html_clean)
    if phone_match:
        phone = phone_match.group(1).strip()

    # Extract LinkedIn link
    linkedin = "https://www.linkedin.com/in/hardik-khandhar-410215124"
    li_match = re.search(r'href="(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)"', html_clean)
    if li_match:
        linkedin = li_match.group(1).strip()

    # Extract Languages
    languages = "English, Hindi, Gujarati (Mother tongue)"
    lang_match = re.search(r'Languages</span>\s*<span class="detail-value">([^<]+)</span>', html_clean)
    if lang_match:
        languages = lang_match.group(1).strip()

    # Format contact numbers
    phone_formatted = phone
    phone_clean = re.sub(r'[^\d+]', '', phone)
    if phone_clean.startswith("+91") and len(phone_clean) == 13:
        phone_formatted = f"+91 {phone_clean[3:8]} {phone_clean[8:]}"
    elif len(phone_clean) == 10:
        phone_formatted = f"+91 {phone_clean[:5]} {phone_clean[5:]}"

    # Extract career summary
    summary = ""
    summary_match = re.search(r'class="about-summary">([^<]+)</p>', html_clean)
    if summary_match:
        summary = " ".join(summary_match.group(1).strip().split())

    # Extract skills
    skills_dict = {}
    skill_parts = html_clean.split('<div class="skill-category-card')
    for part in skill_parts[1:]:
        part_clean = part.split('</section>')[0]
        title_match = re.search(r'<h3 class="skill-card-title">([^<]+)</h3>', part_clean)
        if title_match:
            title = title_match.group(1).strip()
            skills_list = re.findall(r'<span class="skill-name">([^<]+)</span>', part_clean)
            skills_list = [s.strip() for s in skills_list if s.strip()]
            if skills_list:
                skills_dict[title] = skills_list

    # Extract other tooling & integrations
    other_skills_raw = re.findall(r'<span class="skill-tag">(.*?)</span>', html_clean, re.DOTALL)
    other_skills = []
    for s in other_skills_raw:
        s_clean = re.sub(r'<svg.*?</svg>', '', s, flags=re.DOTALL).strip()
        if s_clean:
            other_skills.append(s_clean)

    # Extract experience
    experience_list = []
    exp_parts = html_clean.split('<div class="experience-card-item')
    for part in exp_parts[1:]:
        part_clean = part.split('</section>')[0]
        date_match = re.search(r'<span class="experience-date-tag">([^<]+)</span>', part_clean)
        role_match = re.search(r'<h3 class="experience-role">([^<]+)</h3>', part_clean)
        comp_match = re.search(r'<span class="experience-company">([^<]+)</span>', part_clean)
        
        if date_match and role_match and comp_match:
            bullets = re.findall(r'<div class="achievement-bullet">.*?<span>([^<]+)</span>', part_clean, re.DOTALL)
            bullets = [b.strip() for b in bullets if b.strip()]
            experience_list.append({
                "date": date_match.group(1).strip(),
                "role": role_match.group(1).strip(),
                "company": comp_match.group(1).strip(),
                "bullets": bullets
            })

    # Extract projects from js/projects-data.js
    projects_list = []
    if os.path.exists("js/projects-data.js"):
        with open("js/projects-data.js", "r", encoding="utf-8") as pf:
            js_content = pf.read()
        
        # Clean comments
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        js_content = re.sub(r'//.*?\n', '\n', js_content)
        
        blocks = js_content.split('{')
        for block in blocks[1:]:
            title_m = re.search(r'title:\s*["\'](.*?)["\']', block)
            desc_m = re.search(r'desc:\s*["\'](.*?)["\']', block)
            
            if title_m and desc_m:
                title = title_m.group(1).strip()
                desc = desc_m.group(1).strip()
                
                resp_block_m = re.search(r'responsibilities:\s*\[(.*?)\]', block, re.DOTALL)
                bullets = []
                if resp_block_m:
                    bullets = re.findall(r'["\'](.*?)["\']', resp_block_m.group(1))
                    bullets = [b.strip() for b in bullets if b.strip()]
                
                tech_block_m = re.search(r'tech:\s*\[(.*?)\]', block, re.DOTALL)
                tech = []
                if tech_block_m:
                    tech = re.findall(r'["\'](.*?)["\']', tech_block_m.group(1))
                    tech = [t.strip() for t in tech if t.strip()]
                
                projects_list.append({
                    "title": title,
                    "desc": desc,
                    "bullets": bullets,
                    "tech": tech
                })

    # Extract education
    education_list = []
    edu_matches = re.findall(r'<div class="edu-card">.*?<span class="edu-degree">([^<]+)</span>.*?<span class="edu-year">([^<]+)</span>.*?<div class="edu-school">([^<]+)</div>', html_clean, re.DOTALL)
    for edu in edu_matches:
        education_list.append({
            "degree": edu[0].strip(),
            "year": edu[1].strip(),
            "school": edu[2].strip()
        })

    # 2. Build the ReportLab PDF Document
    pdf_dir = "assets/resume"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "hardik_resume.pdf")

    # Document template with 0.4-inch (28.8 points) margins to fit exactly 1 page
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=28.8,
        rightMargin=28.8,
        topMargin=28.8,
        bottomMargin=28.8
    )

    styles = getSampleStyleSheet()

    # Style setups
    primary_color = colors.HexColor("#1E3A8A")   # Navy / Indigo Accent
    text_color = colors.HexColor("#1F2937")      # Off-black body
    meta_color = colors.HexColor("#4B5563")      # Muted gray for dates/links

    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#111827"),
        alignment=1
    )

    role_style = ParagraphStyle(
        'ResumeRole',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=primary_color,
        alignment=1,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=meta_color,
        alignment=1
    )

    section_heading_style = ParagraphStyle(
        'ResumeSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=primary_color,
        spaceBefore=4,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=text_color
    )

    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=text_color,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=0.5
    )

    job_title_style = ParagraphStyle(
        'ResumeJobTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#111827")
    )

    job_meta_style = ParagraphStyle(
        'ResumeJobMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=meta_color,
        alignment=2
    )

    skills_label_style = ParagraphStyle(
        'ResumeSkillsLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=primary_color
    )

    story = []

    # 1. Header Section
    story.append(Paragraph(name.upper(), name_style))
    story.append(Paragraph(role.upper(), role_style))
    
    # Strip protocol prefix for display
    li_disp = linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
    
    contact_line_1 = f"Email: <a href='mailto:{email}'><font color='#1E3A8A'>{email}</font></a> &nbsp;|&nbsp; " \
                     f"Phone & WhatsApp: <a href='tel:{phone}'><font color='#1E3A8A'>{phone_formatted}</font></a>"
    contact_line_2 = f"Location: {location} &nbsp;|&nbsp; " \
                     f"LinkedIn: <a href='{linkedin}'><font color='#1E3A8A'>{li_disp}</font></a>"
                     
    story.append(Paragraph(contact_line_1, contact_style))
    story.append(Paragraph(contact_line_2, contact_style))
    story.append(Spacer(1, 4))

    def create_section_header(title_text):
        p = Paragraph(title_text.upper(), section_heading_style)
        t = Table([[p]], colWidths=[554])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.75, primary_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    # 2. Professional Summary
    story.append(create_section_header("Professional Summary"))
    story.append(Spacer(1, 2))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 2))

    # 3. Technical Skills
    story.append(create_section_header("Technical Skills"))
    story.append(Spacer(1, 2))
    
    skills_rows = []
    for cat_title, items_list in skills_dict.items():
        label_p = Paragraph(f"{cat_title}:", skills_label_style)
        val_p = Paragraph(", ".join(items_list), body_style)
        skills_rows.append([label_p, val_p])
    
    # Add other integrations
    if other_skills:
        label_p = Paragraph("Tooling & Integrations:", skills_label_style)
        val_p = Paragraph(", ".join(other_skills), body_style)
        skills_rows.append([label_p, val_p])

    # Add Languages
    if languages:
        label_p = Paragraph("Languages:", skills_label_style)
        val_p = Paragraph(languages, body_style)
        skills_rows.append([label_p, val_p])

    skills_table = Table(skills_rows, colWidths=[120, 434])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 2))

    # 4. Professional Experience
    story.append(create_section_header("Professional Experience"))
    story.append(Spacer(1, 2))
    
    for job in experience_list:
        job_left = Paragraph(f"<b>{job['role']}</b> &nbsp;|&nbsp; {job['company']}", job_title_style)
        job_right = Paragraph(job['date'], job_meta_style)
        job_table = Table([[job_left, job_right]], colWidths=[400, 154])
        job_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(job_table)
        
        for bullet in job['bullets']:
            story.append(Paragraph(f"&bull; {bullet}", bullet_style))
        story.append(Spacer(1, 2))

    # 5. Selected Projects
    story.append(create_section_header("Selected Projects"))
    story.append(Spacer(1, 2))
    
    for proj in projects_list:
        tech_str = f"({', '.join(proj['tech'])})" if proj['tech'] else ""
        proj_heading = Paragraph(f"<b>{proj['title']}</b> &mdash; <i>{proj['desc']}</i> <font color='#4B5563'>{tech_str}</font>", body_style)
        story.append(proj_heading)
        story.append(Spacer(1, 1.5))
    story.append(Spacer(1, 2))

    # 6. Education Background
    story.append(create_section_header("Education Background"))
    story.append(Spacer(1, 2))
    
    for edu in education_list:
        edu_left = Paragraph(f"<b>{edu['degree']}</b> &nbsp;|&nbsp; {edu['school']}", body_style)
        edu_right = Paragraph(edu['year'], job_meta_style)
        edu_table = Table([[edu_left, edu_right]], colWidths=[450, 104])
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ]))
        story.append(edu_table)

    # Build PDF
    doc.build(story)
    print(f"Success: PDF resume generated at {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
