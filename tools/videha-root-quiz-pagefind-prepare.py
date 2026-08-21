#!/usr/bin/env python3
"""Prepare only bilingual Videha quiz HTML/HTM from the videha-ejournal.github.io user-site repo."""
from pathlib import Path
import shutil,re,sys
SRC=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
DST=Path(sys.argv[2] if len(sys.argv)>2 else '_pagefind_quiz_build').resolve()
EXCLUDE={'.git','.github','pagefind','pagefind-quiz','_pagefind_quiz_build','node_modules','data'}
QUIZ_STRONG=re.compile(r'''(?:<title[^>]*>[^<]*(?:Videha\s+QUIZ|ई-लर्निङ्ग\s+क्विज|प्रश्नोत्तरी|\bquiz\b)|<h[1-3][^>]*>[^<]*(?:Videha\s+QUIZ|ई-लर्निङ्ग\s+क्विज|प्रश्नोत्तरी|\bquiz\b)|class=[\"'][^\"']*(?:quiz-container|question-card|vq-card|vq-section|kids-quiz|quiz-wrap)[^\"']*[\"']|id=[\"'][^\"']*quiz[^\"']*[\"'])''',re.I|re.S)
def is_quiz_page(raw):
    return bool(QUIZ_STRONG.search(raw))
if DST.exists(): shutil.rmtree(DST)
DST.mkdir(parents=True)
count=0
for p in SRC.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in ('.htm','.html'): continue
    rel=p.relative_to(SRC)
    if any(part in EXCLUDE for part in rel.parts): continue
    raw=p.read_text('utf-8',errors='replace')
    if not is_quiz_page(raw): continue
    if 'data-pagefind-body' not in raw and re.search(r'<body\b',raw,re.I):
        raw=re.sub(r'<body\b','<body data-pagefind-body',raw,count=1,flags=re.I)
    dest=DST/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(raw,encoding='utf-8'); count+=1
print(f'Prepared {count} root user-site Videha quiz HTML/HTM pages')
