# ATLAS: Automated Talent Locator and Assessor System

ATLAS is a resume matching system designed to streamline the hiring process by analyzing job descriptions and candidate resumes.

## Table of Contents
1. [Overview](#overview)
2. [Current Features](#current-features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Input Parameters](#input-parameters)
7. [Output](#output)
8. [Customization](#customization)
9. [Future Improvements](#future-improvements)
10. [Contributing](#contributing)
11. [License](#license)

## Overview

ATLAS uses text processing and pattern matching techniques to analyze job descriptions and resumes. It extracts key skills and information from both job descriptions and resumes using predefined patterns and a skill lexicon, then calculates match scores based on content similarity and skill alignment.

## Current Features

- Skill Lexicon: Utilizes a predefined database of industry-specific skills.
- Text Processing: Uses regular expressions to extract skills and key information.
- Content Analysis: Employs fuzzy string matching for overall relevance assessment.
- Customizable Scoring: Combines skill matching and content relevance with adjustable weights.
- Multi-Document Processing: Handles multiple job descriptions and resumes simultaneously.
- Detailed Reporting: Generates reports on candidate-job matches.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ATLAS.git
   ```
2. Navigate to the ATLAS directory:
   ```
   cd ATLAS
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run ATLAS from the command line:

```
python atlas_resume_matcher.py [options]
```

## Configuration

ATLAS can be configured by modifying the following variables in the script:

- `SKILL_LEXICON`: Dictionary of skills categorized by domain. Modify this to match your industry's specific skill requirements.
- Scoring Weights: Adjust the weights in the `combined_score` calculation to emphasize content or skills more heavily.

## Input Parameters

ATLAS accepts the following command-line arguments:

- `--jd_folder`: Folder containing job description files (default: "job_descriptions")
- `--resume_folder`: Folder containing resume files (default: "resumes")
- `--threshold`: Minimum score for a resume to be considered a match (default: 50.0)
- `--output`: Name of the output file for results (default: "atlas_talent_report.txt")

Example:
```
python atlas_resume_matcher.py --jd_folder custom_jds --resume_folder applicant_resumes --threshold 60 --output results.txt
```

## Output

ATLAS generates a text file (default: `atlas_talent_report.txt`) containing:

- Matched candidates for each job description
- Overall match score for each candidate
- Content alignment score
- Skill match score
- List of relevant skills found in the resume

## Customization

1. Skill Lexicon: Modify the `SKILL_LEXICON` dictionary in the script to add, remove, or modify skill categories and specific skills.
2. Scoring Algorithm: Adjust the weights in the `combined_score` calculation to change the importance of content matching vs. skill matching.
3. Output Format: Modify the output writing section of the script to change the format or add additional information to the report.

## Future Improvements

We plan to enhance ATLAS with more advanced Natural Language Processing (NLP) and Machine Learning (ML) techniques in future iterations:

1. Named Entity Recognition (NER): To automatically identify and extract entities like skills, job titles, and qualifications from unstructured text.
2. Word Embeddings: To capture semantic relationships between skills and job requirements.
3. Topic Modeling: To identify main themes in job descriptions and resumes.
4. Sentence Transformers: For more nuanced similarity comparisons between job descriptions and resumes.
5. Machine Learning Classification: To predict the likelihood of a resume being a good match based on historical hiring data.
6. Skill Taxonomy Learning: To automatically update and expand the skill lexicon.

These enhancements aim to improve ATLAS's accuracy and adaptability to various industries and job markets.

## Contributing

We welcome contributions to ATLAS! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a new Pull Request

Please ensure your code adheres to the project's coding standards and include tests for new features.

## License

ATLAS is released under the MIT License. See the LICENSE file for more details.

---
