@echo off
echo @echo off > Script-install.bat
echo pip install -r requirements.txt >> Script-install.bat

echo @echo off > Script-run.bat
echo :: 运行 Streamlit >> Script-run.bat
echo streamlit run app.py >> Script-run.bat
echo pause >> Script-run.bat

echo @echo off > Script-push.bat
echo git pull >> Script-push.bat
echo git add . >> Script-push.bat
echo git commit -m update >> Script-push.bat
echo git push >> Script-push.bat