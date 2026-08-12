# MEGA E-SAVDO — Django REST Framework + HTML/CSS

Professional marketplace frontend + DRF API. Frontend JavaScriptsiz, Django Templates + CSS orqali ishlaydi.

## Ishga tushirish

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Sayt: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/  
API: http://127.0.0.1:8000/api/

### Muhim
Agar yangi database bo'sh bo'lsa va `DEBUG=True` bo'lsa, bosh sahifaga birinchi kirishda demo ma'lumotlar avtomatik yaratiladi. `python manage.py seed_demo` esa buni qo'lda bajarish uchun ham mavjud.

Demo paketda 12 ta mahsulot uchun lokal rasmlar mavjud.
