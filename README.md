# 🎬 Cinema Booking Website (Django)

## 📌 Project Overview

เว็บไซต์จองตั๋วภาพยนตร์ พัฒนาด้วย **Django Framework**
รองรับการเลือกหนัง เลือกรอบ เลือกที่นั่ง และออกตั๋ว

---

## 📂 Project Structure

```
yzy/
└── yzy/
    └── moviebooking/
        ├── cinema/          # app หลัก (movies, booking)
        ├── media/           # เก็บรูปภาพ
        ├── moviebooking/   # project settings
        ├── db.sqlite3      # database
        ├── manage.py
        └── requirements.txt
```

---

## ⚙️ Features

* 🎬 แสดงรายการภาพยนตร์
* ⏰ เลือกรอบฉาย
* 💺 เลือกที่นั่ง
* 💳 ระบบชำระเงิน
* 🎟️ แสดงตั๋ว
* 👤 ระบบ login / logout

---

## 🛠️ Technologies Used

* Python 3
* Django
* SQLite3
* HTML / CSS / Bootstrap
* JavaScript

---

## 🚀 Installation

### 1. Clone Repository

```
git clone https://github.com/mathuradapha/yzy.git
cd yzy/yzy/moviebooking
```

### 2. Create Virtual Environment

```
python -m venv venv
```

### 3. Activate

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

### 4. Install Dependencies

```
pip install -r requirements.txt
```

### 5. Run Migrations

```
python manage.py migrate
```

### 6. Run Server

```
python manage.py runserver
```

### 7. Open Website

```
http://127.0.0.1:8000/
```

---

## ⚙️ Configuration

* Database: SQLite (default)
* Static & Media files:

```
python manage.py collectstatic
```

---

## 👤 Usage

1. Login เข้าสู่ระบบ
2. เลือกภาพยนตร์
3. เลือกรอบฉาย
4. เลือกที่นั่ง
5. ชำระเงิน
6. รับตั๋ว

---

## 📸 Screenshots

> แนะนำ: เพิ่มรูปจากโปรเจคจริง เช่น

* หน้า Home
* หน้าเลือกหนัง
* หน้าเลือกที่นั่ง
* หน้า Payment
* หน้า Ticket

---

## 🌐 Deployment

โปรเจคสามารถ deploy ได้ เช่น:

* Render
* Railway

---

## 📌 Notes

* ใช้เพื่อการศึกษา
* สามารถต่อยอดเพิ่มระบบจริง เช่น Payment Gateway

---

## 👨‍💻 Author

GitHub: https://github.com/mathuradapha
