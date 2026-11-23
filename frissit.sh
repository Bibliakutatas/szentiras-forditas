#!/bin/bash
python3 audit.py
python3 build_lexicon.py
git add -A
git commit -m "Uj fejezetek es szotar frissitese"
git push
mkdocs gh-deploy
