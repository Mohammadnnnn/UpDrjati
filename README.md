# 🎓 UpDrjati Bot - بوت تيليجرام للجامعات

بوت تيليجرام تعليمي شامل لإدارة المواد الجامعية مع نظام استيراد جماعي كامل.

## ✨ المميزات

✅ **نظام استيراد جماعي** - استيراد الجامعات والمواد بشكل مجمع
✅ **قاعدة بيانات SQLite** - تُنشأ تلقائياً
✅ **نظام نقاط** - مكافآت للمستخدمين
✅ **نظام إحالة** - كود إحالة لكل مستخدم
✅ **لوحة أدمن كاملة** - إدارة شاملة
✅ **ملف واحد** - كل شيء في `telegram_bot_all_in_one.py`

---

## 🚀 التشغيل السريع

### **الطريقة 1: على جهازك المحلي**

```bash
# 1. استنساخ المشروع
git clone https://github.com/Mohammadnnnn/UpDrjati.git
cd UpDrjati

# 2. تثبيت المكتبات
pip install -r requirements.txt

# 3. تشغيل البوت
python3 telegram_bot_all_in_one.py
```

**ملاحظة:** التوكن موجود بالفعل في الملف!

---

### **الطريقة 2: على PythonAnywhere (مجاني)**

1. اذهب إلى: https://www.pythonanywhere.com/
2. أنشئ حساب مجاني
3. افتح **Bash console**
4. نفّذ:

```bash
git clone https://github.com/Mohammadnnnn/UpDrjati.git
cd UpDrjati
pip3 install --user -r requirements.txt
python3 telegram_bot_all_in_one.py
```

5. البوت يعمل الآن! ✅

---

### **الطريقة 3: على Railway (سهل)**

1. اذهب إلى: https://railway.app/
2. سجل دخول بحساب GitHub
3. **New Project** → **Deploy from GitHub repo**
4. اختر `Mohammadnnnn/UpDrjati`
5. اختر البرانش (أو اترك الـ main)
6. Railway سيكتشف `Procfile` تلقائياً
7. اضغط **Deploy**! 🚀

---

### **الطريقة 4: على Render (مجاني)**

1. اذهب إلى: https://render.com/
2. **New** → **Background Worker**
3. Connect GitHub → اختر المستودع
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `python3 telegram_bot_all_in_one.py`
6. **Create Web Service**

---

## 📱 استخدام البوت

### **للمستخدمين:**

```
/start - بدء البوت
/help - المساعدة
```

ثم استخدم الأزرار:
- 📚 تصفح المواد
- 🔍 بحث سريع
- 💰 نقاطي
- ❓ المساعدة

---

### **للأدمن:**

```
/adminhelp - دليل الأدمن الكامل
/import - الاستيراد الجماعي التفاعلي
/importunis - استيراد جامعات
/importcourses - استيراد مواد
/adduni CODE NAME - إضافة جامعة
/stats - الإحصائيات
/listids unis - عرض الجامعات
```

---

## 📥 الاستيراد الجماعي

### **استيراد الجامعات:**

**طريقة 1: نص مباشر**
```
/importunis QU,جامعة قطر;KSU,جامعة الملك سعود
```

**طريقة 2: ملف CSV**

أنشئ ملف `universities.csv`:
```csv
code,name,description,location,website
QU,جامعة قطر,جامعة حكومية,الدوحة,qu.edu.qa
KSU,جامعة الملك سعود,جامعة حكومية,الرياض,ksu.edu.sa
```

ثم:
```
/import
→ اختر "استيراد جامعات"
→ أرسل الملف
```

---

### **استيراد المواد:**

**طريقة 1: نص مباشر**
```
/importcourses QU,CS101,البرمجة,د.أحمد;QU,CS102,قواعد البيانات
```

**طريقة 2: ملف CSV**

أنشئ ملف `courses.csv`:
```csv
university_code,course_code,course_name,instructor,credits,semester
QU,CS101,مقدمة في البرمجة,د.أحمد,3,Fall 2024
QU,CS102,قواعد البيانات,د.محمد,3,Spring 2025
```

ثم:
```
/import
→ اختر "استيراد مواد"
→ أرسل الملف
```

---

## 🔧 الإعدادات

### **تغيير التوكن:**

افتح `telegram_bot_all_in_one.py` في السطر 83:

```python
BOT_TOKEN = "YOUR_TOKEN_HERE"
BOT_USERNAME = "YourBotUsername"
```

### **تغيير IDs الأدمن:**

في السطر 87:

```python
ADMIN_IDS = [123456789, 987654321]  # ضع IDs الأدمن
```

---

## 📂 البنية التلقائية

عند تشغيل البوت لأول مرة، يتم إنشاء:

```
UpDrjati/
├── telegram_bot_all_in_one.py  ← الملف الرئيسي
├── requirements.txt            ← المكتبات المطلوبة
├── data/
│   ├── database/
│   │   └── university_courses.db  ← قاعدة البيانات
│   ├── backups/
│   └── files/
├── logs/
│   └── bot.log  ← سجل العمليات
├── exports/
└── imports/
```

---

## ⚙️ المكتبات المستخدمة

- `python-telegram-bot==20.7` - مكتبة Telegram Bot
- `nest-asyncio` - دعم async
- `aiofiles` - ملفات async
- `sqlite3` - قاعدة البيانات (مدمجة في Python)

---

## 🐛 حل المشاكل

### **"Invalid token"**
- تأكد من التوكن في السطر 83
- احصل على توكن جديد من @BotFather

### **"Module not found"**
```bash
pip install -r requirements.txt
```

### **"403 Forbidden"**
- البيئة الحالية محظورة من Telegram
- شغّل البوت على بيئة أخرى (انظر طرق التشغيل أعلاه)

### **"Database locked"**
- أغلق أي نسخة أخرى من البوت
- امسح ملف `data/database/university_courses.db-wal`

---

## 📞 الدعم

- البوت: [@UpDrjati_Bot](https://t.me/UpDrjati_Bot)
- المستودع: [GitHub](https://github.com/Mohammadnnnn/UpDrjati)
- الواتساب: +974 39988411

---

## 📝 الترخيص

هذا المشروع مفتوح المصدر للأغراض التعليمية.

---

## 🎉 شكر خاص

تم تطوير هذا البوت بمساعدة Claude Code.

**استمتع! 🚀**
