# 🚚 Delivery FastAPI App

FastAPI yordamida ishlab chiqilayotgan Delivery REST API loyihasi.

Loyiha foydalanuvchilar (`accounts`) va mahsulotlar (`products`) bilan
ishlash uchun mo‘ljallangan. Ma’lumotlar MySQL database'da saqlanadi.

---

## 🛠 Technologies

- Python
- FastAPI `0.141.1`
- SQLAlchemy
- MySQL
- AsyncMy
- Pydantic
- Uvicorn
- SQLAlchemy Utils
- python-dotenv

---

## 📁 Project Structure

```text
delivery_fastAPI_app/
│
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
│
├── products/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
│
├── .env
├── .gitignore
├── database.py
├── init_db.py
├── main.py
├── README.md
└── requirements.txt