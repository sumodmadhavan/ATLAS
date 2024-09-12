"""
ATLAS: Automated Talent Locator and Assessor System
Author: Sumod Sethumadhavan
Version: 1.0.0
Created: 12-09-2024

MIT License

Copyright (c) [Current Year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
import struct
import docx2txt
from fuzzywuzzy import fuzz
from pdfminer.high_level import extract_text
import argparse
from collections import defaultdict

print("""
   ___  ________ ___    ___   _____
  / _ |/_  __/ // / |  / / | / / _ \\
 / __ | / / / _  /| | / /| |/ / ___/
/_/ |_|/_/ /_//_/ |_|/_/ |___/_/    
                                    
Automated Talent Locator and Assessor System
""")

# Previous helper functions remain the same
def preprocess_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def fuzzy_match_score(text1, text2):
    return fuzz.token_set_ratio(text1, text2)

def read_doc(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
        if content.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
            return extract_text_from_doc(content)
        return content.decode("utf-8", errors="ignore")

def extract_text_from_doc(content):
    text = ""
    try:
        pos = 0
        while True:
            pos = content.find(b"\x00\x00\x00", pos)
            if pos == -1:
                break
            pos += 3
            chunk_len = struct.unpack("<I", content[pos : pos + 4])[0]
            pos += 4
            chunk = content[pos : pos + chunk_len]
            text += chunk.decode("utf-16le", errors="ignore")
            pos += chunk_len
    except:
        pass
    return text

def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    try:
        if ext.lower() == ".docx":
            return docx2txt.process(file_path)
        elif ext.lower() == ".pdf":
            return extract_text(file_path)
        elif ext.lower() == ".doc":
            return read_doc(file_path)
        elif ext.lower() == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return ""

SKILL_LEXICON = {
    'Programming Languages': ['Python', 'Java', 'C++', 'JavaScript', 'Ruby', 'Go', 'Rust', 'PHP', 'Swift', 'Kotlin'],
    'Web Technologies': ['HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring Boot'],
    'Databases': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis', 'Elasticsearch'],
    'Cloud Platforms': ['AWS', 'Azure', 'Google Cloud', 'Heroku', 'DigitalOcean'],
    'DevOps': ['Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'Terraform', 'Ansible'],
    'Machine Learning': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'NLTK', 'OpenCV'],
    'Data Analysis': ['Pandas', 'NumPy', 'R', 'Tableau', 'Power BI', 'SAS'],
    'Project Management': ['Agile', 'Scrum', 'Kanban', 'JIRA', 'Trello', 'MS Project'],
    'Version Control': ['Git', 'SVN', 'Mercurial'],
    'Testing': ['JUnit', 'Selenium', 'Pytest', 'Jasmine', 'Mocha'],
    'Soft Skills': ['Communication', 'Teamwork', 'Problem Solving', 'Time Management', 'Leadership']
}

def extract_skills_from_text(text):
    skills = set()
    text_lower = text.lower()
    for category, category_skills in SKILL_LEXICON.items():
        for skill in category_skills:
            if skill.lower() in text_lower:
                skills.add(skill)
    return skills

def calculate_skill_match(job_skills, resume_skills):
    matched_skills = job_skills.intersection(resume_skills)
    return len(matched_skills) / len(job_skills) if job_skills else 0

def match_resumes_to_jds(base_folder, resume_folder, jd_folder, output_file, threshold):
    jd_path = os.path.join(base_folder, jd_folder)
    if not os.path.exists(jd_path):
        print(f"Job descriptions folder not found: {jd_path}")
        return

    job_descriptions = {}
    jd_skills = {}

    print("ATLAS: Analyzing job descriptions...")
    for filename in os.listdir(jd_path):
        if filename.endswith('.docx'):
            file_path = os.path.join(jd_path, filename)
            jd_text = read_file(file_path)
            if jd_text:
                job_descriptions[filename] = jd_text
                skills = extract_skills_from_text(jd_text)
                jd_skills[filename] = skills
                print(f"ATLAS: Extracted skills from {filename}: {skills}")

    if not job_descriptions:
        print(f"ATLAS: No valid job descriptions found in {jd_path}")
        return

    matched_resumes = defaultdict(list)
    resumes_path = os.path.join(base_folder, resume_folder)
    
    if not os.path.exists(resumes_path):
        print(f"ATLAS: Resumes folder not found: {resumes_path}")
        return

    print("ATLAS: Commencing resume analysis...")
    for filename in os.listdir(resumes_path):
        file_path = os.path.join(resumes_path, filename)
        print(f"ATLAS: Processing resume: {filename}")
        resume_text = read_file(file_path)
        if resume_text:
            preprocessed_resume = preprocess_text(resume_text)
            resume_skills = extract_skills_from_text(resume_text)
            print(f"ATLAS: Extracted skills from resume {filename}: {resume_skills}")
            
            for jd_name, jd_text in job_descriptions.items():
                preprocessed_jd = preprocess_text(jd_text)
                content_score = fuzzy_match_score(preprocessed_resume, preprocessed_jd)
                skill_score = calculate_skill_match(jd_skills[jd_name], resume_skills) * 100
                combined_score = (content_score * 0.6 + skill_score * 0.4)  # Adjusted weights
                
                print(f"ATLAS: Match scores for {filename} against {jd_name}:")
                print(f"  Content score: {content_score:.2f}")
                print(f"  Skill score: {skill_score:.2f}")
                print(f"  Combined score: {combined_score:.2f}")
                
                if combined_score >= threshold:
                    matched_resumes[jd_name].append((filename, combined_score, content_score, skill_score))
        else:
            print(f"ATLAS: Skipping {filename} due to reading error")

    output_path = os.path.join(base_folder, output_file)
    print(f"ATLAS: Generating talent assessment report...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("ATLAS: Automated Talent Locator and Assessor System\n")
        f.write("Talent Assessment Report\n\n")
        for jd_name, matches in matched_resumes.items():
            f.write(f"Potential Candidates for {jd_name}:\n")
            for filename, combined_score, content_score, skill_score in sorted(matches, key=lambda x: x[1], reverse=True):
                f.write(f"Candidate: {filename}\n")
                f.write(f"  Overall Match Score: {combined_score:.2f}\n")
                f.write(f"  Content Alignment: {content_score:.2f}\n")
                f.write(f"  Skill Match: {skill_score:.2f}\n")
                f.write(f"  Relevant Skills: {jd_skills[jd_name].intersection(extract_skills_from_text(read_file(os.path.join(resumes_path, filename))))}\n\n")
            f.write("\n")

    print(f"ATLAS: Analysis complete. Processed {len(os.listdir(resumes_path))} resumes against {len(job_descriptions)} job descriptions.")
    print(f"ATLAS: Talent assessment report generated at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATLAS: Automated Talent Locator and Assessor System")
    parser.add_argument("--jd_folder", default="job_descriptions", help="Folder containing job description files")
    parser.add_argument("--threshold", type=float, default=50.0, help="Matching threshold score")
    parser.add_argument("--resume_folder", default="resumes", help="Folder containing resumes")
    parser.add_argument("--output", default="atlas_talent_report.txt", help="Output file name")
    
    args = parser.parse_args()

    base_folder = os.getcwd()
    
    match_resumes_to_jds(
        base_folder, 
        args.resume_folder, 
        args.jd_folder, 
        args.output, 
        args.threshold
    )