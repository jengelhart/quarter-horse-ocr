This is a simple script meant to scrape quarter-horse race
data from Equibase pdfs. It uses pytesseract for OCR. This
script does not yield perfectly clean data, as OCR creates
inconsistencies.

Usage:
1) install all dependencies with 'pip3 install'
2) place pdfs in same directory as script
3) run with 'python3 parse_chart.py chart_name.pdf'
4) output will be 'chart_name-data.csv'
