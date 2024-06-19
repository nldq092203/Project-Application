
python -m venv env
.\env\Scripts\activate 
.\env\Scripts\python.exe -m pip install --upgrade pip

pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input