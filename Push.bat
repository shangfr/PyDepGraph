@echo off
echo @echo off > run.bat
echo streamlit run app.py >> run.bat
git pull
git add .
git commit -m update
git push

