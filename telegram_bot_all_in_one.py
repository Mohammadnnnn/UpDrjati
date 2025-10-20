#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
🎓 TELEGRAM EDUCATIONAL BOT - ALL IN ONE FILE
═══════════════════════════════════════════════════════════════════════════════
Version: 13.0 COMPLETE
✅ كل شيء في ملف واحد
✅ يعمل مباشرة بدون ملفات إضافية
✅ نظام استيراد جماعي كامل
✅ جاهز للعمل على Claude Code و GitHub
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 1: تثبيت المكتبات تلقائياً
# ═══════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import os

def install_packages():
    """تثبيت المكتبات المطلوبة تلقائياً"""
    packages = [
        'python-telegram-bot==20.7',
        'nest-asyncio',
        'aiofiles'
    ]
    
    print("📦 جاري تثبيت المكتبات المطلوبة...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        except:
            print(f"⚠️ تعذر تثبيت {package}")
    print("✅ تم تثبيت المكتبات!")

# تثبيت المكتبات
try:
    import telegram
except ImportError:
    install_packages()

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 2: الاستيرادات
# ═══════════════════════════════════════════════════════════════════════════

import logging
import sqlite3
import json
import csv
import io
import hashlib
import random
import asyncio
import traceback
import html
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple
from functools import wraps
from pathlib import Path

import nest_asyncio
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    Poll, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    PollAnswerHandler, ContextTypes, MessageHandler,
    filters, ConversationHandler
)
from telegram.constants import ParseMode

nest_asyncio.apply()

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 3: الإعدادات - غيّر هذه فقط!
# ═══════════════════════════════════════════════════════════════════════════

# ⚠️ ضع التوكن الخاص بك هنا
BOT_TOKEN = "7718993072:AAHDzMdT70xfnVwif-BV-2XsO_Kvnq4OyW4"
BOT_USERNAME = "UpDrjati_Bot"

# IDs المسؤولين
ADMIN_IDS = [535023010, 6149033425]  # يمكنك تغيير هذه
SUPER_ADMIN_ID = 6149033425
ADMIN_WHATSAPP = "97439988411"

# نظام النقاط
POINTS_CONFIG = {
    'download_file': 5,
    'download_message': 3,
    'referral_bonus': 100,
    'referred_bonus': 50,
    'quiz_correct': 10,
    'quiz_wrong': -2,
    'favorite_add': 2,
    'daily_bonus': 20
}

# حالات المحادثة
(ADD_UNI_CODE, ADD_UNI_NAME, ADD_COURSE_UNI, ADD_COURSE_CODE, 
 ADD_COURSE_NAME, ADD_COURSE_INSTRUCTOR, ADD_FILE_COURSE, 
 ADD_FILE_UPLOAD, ADD_MSG_COURSE, ADD_MSG_TITLE, ADD_MSG_CONTENT,
 IMPORT_TYPE, IMPORT_FILE) = range(13)

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 4: إعداد المجلدات والسجلات
# ═══════════════════════════════════════════════════════════════════════════

# إنشاء المجلدات المطلوبة
BASE_DIR = Path.cwd()
DIRS = ['data', 'data/database', 'data/backups', 'data/files', 'logs', 'exports', 'imports']
for dir_path in DIRS:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

DATABASE_PATH = BASE_DIR / 'data' / 'database' / 'university_courses.db'
LOG_PATH = BASE_DIR / 'logs' / 'bot.log'

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 5: قاعدة البيانات
# ═══════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """مدير قاعدة البيانات مع الاستيراد الجماعي"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الجامعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS universities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                location TEXT DEFAULT '',
                website TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المواد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                university_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT DEFAULT 'جميع الدكاترة',
                credits TEXT DEFAULT '3',
                semester TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE,
                UNIQUE(university_id, code, name)
            )
        ''')
        
        # جدول الملفات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                file_id TEXT NOT NULL,
                file_name TEXT DEFAULT '',
                file_size INTEGER DEFAULT 0,
                file_path TEXT DEFAULT '',
                file_content TEXT DEFAULT '',
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        ''')
        
        # جدول الرسائل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        ''')
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT DEFAULT '',
                points INTEGER DEFAULT 0,
                total_earned INTEGER DEFAULT 0,
                referral_code TEXT UNIQUE,
                referred_by INTEGER,
                referral_count INTEGER DEFAULT 0,
                is_admin INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referred_by) REFERENCES users (user_id)
            )
        ''')
        
        # جدول المفضلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (course_id) REFERENCES courses(id),
                UNIQUE(user_id, course_id)
            )
        ''')
        
        # جدول تاريخ النقاط
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS points_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points_change INTEGER NOT NULL,
                reason TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # إضافة بيانات أولية
        cursor.execute("INSERT OR IGNORE INTO universities (code, name) VALUES ('QU', 'جامعة قطر')")
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized")
    
    # ═══════════════════════════════════════════════════════════════════════
    # دوال الاستيراد الجماعي
    # ═══════════════════════════════════════════════════════════════════════
    
    def import_universities_csv(self, csv_content: str) -> Dict[str, Any]:
        """استيراد الجامعات من CSV"""
        results = {'total': 0, 'success': 0, 'failed': 0, 'errors': []}
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # محاولة قراءة CSV
            csv_file = io.StringIO(csv_content)
            reader = csv.reader(csv_file)
            
            for row_num, row in enumerate(reader, 1):
                if row_num == 1 and 'code' in str(row).lower():
                    continue  # تخطي العناوين
                
                if not row or len(row) < 2:
                    continue
                    
                results['total'] += 1
                
                try:
                    code = row[0].strip().upper()
                    name = row[1].strip()
                    description = row[2].strip() if len(row) > 2 else ''
                    location = row[3].strip() if len(row) > 3 else ''
                    website = row[4].strip() if len(row) > 4 else ''
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO universities 
                        (code, name, description, location, website)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (code, name, description, location, website))
                    
                    if cursor.rowcount > 0:
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Row {row_num}: Already exists")
                        
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Row {row_num}: {str(e)}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            results['errors'].append(f"Fatal error: {str(e)}")
            
        return results
    
    def import_courses_csv(self, csv_content: str) -> Dict[str, Any]:
        """استيراد المواد من CSV"""
        results = {'total': 0, 'success': 0, 'failed': 0, 'errors': []}
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # الحصول على خريطة الجامعات
            cursor.execute('SELECT id, code FROM universities')
            uni_map = {row[1]: row[0] for row in cursor.fetchall()}
            
            csv_file = io.StringIO(csv_content)
            reader = csv.reader(csv_file)
            
            for row_num, row in enumerate(reader, 1):
                if row_num == 1 and 'code' in str(row).lower():
                    continue
                
                if not row or len(row) < 3:
                    continue
                    
                results['total'] += 1
                
                try:
                    uni_code = row[0].strip().upper()
                    course_code = row[1].strip().upper()
                    course_name = row[2].strip()
                    instructor = row[3].strip() if len(row) > 3 else 'جميع الدكاترة'
                    credits = row[4].strip() if len(row) > 4 else '3'
                    semester = row[5].strip() if len(row) > 5 else ''
                    
                    if uni_code not in uni_map:
                        results['failed'] += 1
                        results['errors'].append(f"Row {row_num}: University {uni_code} not found")
                        continue
                    
                    uni_id = uni_map[uni_code]
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO courses 
                        (university_id, code, name, instructor, credits, semester)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (uni_id, course_code, course_name, instructor, credits, semester))
                    
                    if cursor.rowcount > 0:
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Row {row_num}: Already exists")
                        
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Row {row_num}: {str(e)}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            results['errors'].append(f"Fatal error: {str(e)}")
            
        return results
    
    # ═══════════════════════════════════════════════════════════════════════
    # دوال قاعدة البيانات الأساسية
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_user(self, user_id: int, username: str, first_name: str):
        """إضافة مستخدم جديد"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            referral_code = hashlib.md5(f"{user_id}{datetime.now()}".encode()).hexdigest()[:8].upper()
            
            cursor.execute('''
                INSERT OR IGNORE INTO users 
                (user_id, username, first_name, referral_code)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, f"REF{referral_code}"))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_user(self, user_id: int):
        """الحصول على بيانات مستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'user_id': result[0],
                    'username': result[1],
                    'first_name': result[2],
                    'points': result[4],
                    'referral_code': result[6]
                }
            return None
        except:
            return None
    
    def get_all_universities(self):
        """الحصول على جميع الجامعات"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, code, name FROM universities ORDER BY code')
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def get_courses_by_university(self, uni_id: int):
        """الحصول على مواد جامعة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, code, name, instructor 
                FROM courses 
                WHERE university_id = ?
                ORDER BY code
            ''', (uni_id,))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def get_files_by_course(self, course_id: int):
        """الحصول على ملفات مادة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, file_type, file_id, file_name 
                FROM files 
                WHERE course_id = ?
            ''', (course_id,))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def get_messages_by_course(self, course_id: int):
        """الحصول على رسائل مادة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, content, created_at 
                FROM messages 
                WHERE course_id = ?
            ''', (course_id,))
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            return []

# إنشاء مدير قاعدة البيانات
db = DatabaseManager()

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 6: معالج الأخطاء
# ═══════════════════════════════════════════════════════════════════════════

def handle_errors(func):
    """معالج أخطاء عام"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            
            try:
                if len(args) > 0:
                    update = args[0]
                    if hasattr(update, 'message') and update.message:
                        await update.message.reply_text("❌ حدث خطأ مؤقت")
                    elif hasattr(update, 'callback_query') and update.callback_query:
                        await update.callback_query.answer("❌ خطأ", show_alert=True)
            except:
                pass
    return wrapper

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 7: الأوامر الأساسية
# ═══════════════════════════════════════════════════════════════════════════

@handle_errors
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البداية"""
    user = update.effective_user
    
    # إضافة المستخدم
    db.add_user(user.id, user.username or "", user.first_name or "User")
    
    text = f"🎓 <b>مرحباً في بوت الجامعات التعليمي!</b>\n\n"
    text += f"👋 أهلاً {html.escape(user.first_name)}\n\n"
    text += f"📱 استخدم الأزرار للتنقل:\n"
    text += f"• 📚 تصفح المواد\n"
    text += f"• 🔍 البحث السريع\n"
    text += f"• 💰 نقاطك\n"
    text += f"• ❓ المساعدة"
    
    keyboard = [
        [KeyboardButton("📚 تصفح المواد"), KeyboardButton("🔍 بحث سريع")],
        [KeyboardButton("💰 نقاطي"), KeyboardButton("❓ المساعدة")]
    ]
    
    if user.id in ADMIN_IDS:
        keyboard.append([KeyboardButton("👑 لوحة الأدمن")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

@handle_errors
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر المساعدة"""
    text = """
❓ <b>المساعدة</b>

<b>للمستخدمين:</b>
/start - بدء البوت
/help - هذه المساعدة

<b>للبحث:</b>
أرسل: الجامعة المادة
مثال: QU CS101

<b>النقاط:</b>
• تحميل ملف: +5 نقاط
• عرض رسالة: +3 نقاط
• إحالة صديق: +100 نقاط
"""
    
    if update.effective_user.id in ADMIN_IDS:
        text += """
<b>للأدمن:</b>
/adminhelp - دليل الأدمن الكامل
/import - الاستيراد الجماعي
/stats - الإحصائيات
"""
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

@handle_errors
async def adminhelp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دليل الأدمن"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    text = """
👑 <b>دليل الأدمن الكامل</b>

<b>📥 الاستيراد الجماعي:</b>
/import - واجهة الاستيراد
/importunis - استيراد جامعات
/importcourses - استيراد مواد

<b>➕ الإضافة السريعة:</b>
/adduni CODE NAME - إضافة جامعة
/addcourse UNI_CODE COURSE NAME - إضافة مادة

<b>📊 المعلومات:</b>
/stats - الإحصائيات
/listids unis - عرض الجامعات
/listids courses - عرض المواد

<b>📁 تنسيق CSV للاستيراد:</b>

<b>الجامعات:</b>
<code>code,name,description,location,website
QU,جامعة قطر,وصف,الدوحة,qu.edu.qa</code>

<b>المواد:</b>
<code>university_code,course_code,course_name,instructor
QU,CS101,البرمجة,د.أحمد</code>
"""
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 8: أوامر الاستيراد الجماعي
# ═══════════════════════════════════════════════════════════════════════════

@handle_errors
async def import_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """واجهة الاستيراد التفاعلية"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("🏛️ استيراد جامعات", callback_data="import_unis")],
        [InlineKeyboardButton("📚 استيراد مواد", callback_data="import_courses")],
        [InlineKeyboardButton("❌ إلغاء", callback_data="cancel")]
    ]
    
    await update.message.reply_text(
        "📥 <b>الاستيراد الجماعي</b>\n\nاختر نوع الاستيراد:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    
    return IMPORT_TYPE

@handle_errors
async def import_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج اختيار نوع الاستيراد"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "cancel":
        await query.edit_message_text("❌ تم الإلغاء")
        return ConversationHandler.END
    
    context.user_data['import_type'] = data
    
    if data == "import_unis":
        text = """
🏛️ <b>استيراد الجامعات</b>

أرسل ملف CSV بالتنسيق:
<code>code,name,description,location,website</code>

مثال:
<code>QU,جامعة قطر,وصف,الدوحة,qu.edu.qa
KSU,جامعة الملك سعود,وصف,الرياض,ksu.edu.sa</code>
"""
    else:
        text = """
📚 <b>استيراد المواد</b>

أرسل ملف CSV بالتنسيق:
<code>university_code,course_code,course_name,instructor</code>

مثال:
<code>QU,CS101,البرمجة,د.أحمد
QU,CS102,قواعد البيانات,د.محمد</code>
"""
    
    await query.edit_message_text(
        text + "\n\n📎 أرسل الملف الآن:",
        parse_mode=ParseMode.HTML
    )
    
    return IMPORT_FILE

@handle_errors
async def import_file_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج استقبال ملف الاستيراد"""
    import_type = context.user_data.get('import_type')
    
    if not update.message.document:
        await update.message.reply_text("❌ الرجاء إرسال ملف CSV")
        return IMPORT_FILE
    
    document = update.message.document
    
    if not document.file_name.endswith('.csv'):
        await update.message.reply_text("❌ الملف يجب أن يكون CSV")
        return IMPORT_FILE
    
    status_msg = await update.message.reply_text("⏳ جاري المعالجة...")
    
    try:
        # تحميل الملف
        file = await context.bot.get_file(document.file_id)
        file_bytes = await file.download_as_bytearray()
        
        # محاولة فك التشفير
        csv_content = None
        for encoding in ['utf-8', 'utf-8-sig', 'cp1256', 'iso-8859-1']:
            try:
                csv_content = file_bytes.decode(encoding)
                break
            except:
                continue
        
        if not csv_content:
            await status_msg.edit_text("❌ لا يمكن قراءة الملف")
            return ConversationHandler.END
        
        # المعالجة حسب النوع
        if import_type == "import_unis":
            results = db.import_universities_csv(csv_content)
            title = "استيراد الجامعات"
        else:
            results = db.import_courses_csv(csv_content)
            title = "استيراد المواد"
        
        # عرض النتائج
        text = f"📊 <b>نتائج {title}</b>\n\n"
        text += f"📥 الإجمالي: {results['total']}\n"
        text += f"✅ نجح: {results['success']}\n"
        text += f"❌ فشل: {results['failed']}\n"
        
        if results['errors'] and len(results['errors']) <= 5:
            text += f"\n⚠️ الأخطاء:\n"
            for error in results['errors'][:5]:
                text += f"• {error}\n"
        
        await status_msg.edit_text(text, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Import error: {e}")
        await status_msg.edit_text(f"❌ خطأ: {str(e)}")
    
    return ConversationHandler.END

@handle_errors
async def importunis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استيراد سريع للجامعات"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text(
            "🏛️ <b>استيراد جامعات</b>\n\n"
            "أرسل ملف CSV أو:\n"
            "<code>/importunis QU,جامعة قطر;KSU,جامعة الملك سعود</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # معالجة البيانات المباشرة
    data = ' '.join(context.args)
    csv_lines = []
    
    for entry in data.split(';'):
        parts = entry.split(',')
        if len(parts) >= 2:
            csv_lines.append(','.join(parts))
    
    if csv_lines:
        csv_content = '\n'.join(csv_lines)
        results = db.import_universities_csv(csv_content)
        
        text = f"🏛️ نتائج الاستيراد:\n"
        text += f"✅ نجح: {results['success']}\n"
        text += f"❌ فشل: {results['failed']}"
        
        await update.message.reply_text(text)

@handle_errors
async def importcourses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استيراد سريع للمواد"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text(
            "📚 <b>استيراد مواد</b>\n\n"
            "أرسل ملف CSV أو:\n"
            "<code>/importcourses QU,CS101,البرمجة,د.أحمد;QU,CS102,قواعد البيانات</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    data = ' '.join(context.args)
    csv_lines = []
    
    for entry in data.split(';'):
        parts = entry.split(',')
        if len(parts) >= 3:
            csv_lines.append(','.join(parts))
    
    if csv_lines:
        csv_content = '\n'.join(csv_lines)
        results = db.import_courses_csv(csv_content)
        
        text = f"📚 نتائج الاستيراد:\n"
        text += f"✅ نجح: {results['success']}\n"
        text += f"❌ فشل: {results['failed']}"
        
        await update.message.reply_text(text)

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 9: أوامر إضافية للأدمن
# ═══════════════════════════════════════════════════════════════════════════

@handle_errors
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الإحصائيات"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        queries = {
            'المستخدمين': 'SELECT COUNT(*) FROM users',
            'الجامعات': 'SELECT COUNT(*) FROM universities',
            'المواد': 'SELECT COUNT(*) FROM courses',
            'الملفات': 'SELECT COUNT(*) FROM files',
            'الرسائل': 'SELECT COUNT(*) FROM messages'
        }
        
        for key, query in queries.items():
            cursor.execute(query)
            stats[key] = cursor.fetchone()[0]
        
        conn.close()
        
        text = "📊 <b>إحصائيات البوت</b>\n\n"
        for key, value in stats.items():
            text += f"• {key}: {value}\n"
        
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

@handle_errors
async def listids_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض IDs"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text(
            "استخدام:\n"
            "/listids unis - عرض الجامعات\n"
            "/listids courses - عرض المواد"
        )
        return
    
    list_type = context.args[0].lower()
    
    if list_type == 'unis':
        unis = db.get_all_universities()
        if not unis:
            await update.message.reply_text("لا توجد جامعات")
            return
        
        text = "🏛️ <b>الجامعات:</b>\n\n"
        for uni_id, code, name in unis[:20]:
            text += f"🆔 {uni_id} | {code} - {name}\n"
        
        if len(unis) > 20:
            text += f"\n... و {len(unis) - 20} أخرى"
        
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    
    elif list_type == 'courses':
        # يحتاج لتحديد الجامعة
        await update.message.reply_text("قريباً...")

@handle_errors
async def adduni_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إضافة جامعة سريعة"""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ للمسؤولين فقط")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "استخدام:\n<code>/adduni CODE NAME</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    code = context.args[0].upper()
    name = ' '.join(context.args[1:])
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO universities (code, name) VALUES (?, ?)',
            (code, name)
        )
        uni_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            f"✅ تمت إضافة الجامعة!\n\n"
            f"🆔 ID: {uni_id}\n"
            f"📝 Code: {code}\n"
            f"🏛️ Name: {name}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 10: معالج الرسائل النصية
# ═══════════════════════════════════════════════════════════════════════════

@handle_errors
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل النصية"""
    text = update.message.text
    user = update.effective_user
    
    # التأكد من وجود المستخدم
    if not db.get_user(user.id):
        db.add_user(user.id, user.username or "", user.first_name or "")
    
    # معالجة الأزرار
    if text == "📚 تصفح المواد":
        unis = db.get_all_universities()
        if not unis:
            await update.message.reply_text("⚠️ لا توجد جامعات حالياً")
            return
        
        keyboard = []
        for uni_id, code, name in unis:
            keyboard.append([InlineKeyboardButton(
                f"🏛️ {code} - {name}",
                callback_data=f"uni:{uni_id}"
            )])
        
        await update.message.reply_text(
            "🏛️ <b>اختر الجامعة:</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    
    elif text == "💰 نقاطي":
        user_data = db.get_user(user.id)
        if user_data:
            await update.message.reply_text(
                f"💰 نقاطك: {user_data.get('points', 0)}"
            )
        else:
            await update.message.reply_text("❌ لا توجد بيانات")
    
    elif text == "❓ المساعدة":
        await help_command(update, context)
    
    elif text == "👑 لوحة الأدمن" and user.id in ADMIN_IDS:
        await show_admin_panel(update)
    
    else:
        # محاولة البحث
        parts = text.strip().upper().split()
        if len(parts) == 2:
            await update.message.reply_text(f"🔍 البحث عن {parts[0]} {parts[1]}...")
        else:
            await update.message.reply_text("استخدم القائمة أو ابحث: QU CS101")

async def show_admin_panel(update):
    """عرض لوحة الأدمن"""
    keyboard = [
        [InlineKeyboardButton("📥 الاستيراد الجماعي", callback_data="import_menu")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton("🏛️ الجامعات", callback_data="list_unis")],
        [InlineKeyboardButton("❌ إغلاق", callback_data="close")]
    ]
    
    await update.message.reply_text(
        "👑 <b>لوحة تحكم الأدمن</b>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 11: معالج الأزرار (Callbacks)
# ═══════════════════════════════════════════════════════════════════════════

@handle_errors
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأزرار"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "close":
        await query.message.delete()
    
    elif data == "import_menu":
        keyboard = [
            [InlineKeyboardButton("🏛️ استيراد جامعات", callback_data="import_unis_start")],
            [InlineKeyboardButton("📚 استيراد مواد", callback_data="import_courses_start")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")]
        ]
        await query.edit_message_text(
            "📥 <b>الاستيراد الجماعي</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    
    elif data == "stats":
        # عرض الإحصائيات
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM universities')
            unis_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM courses')
            courses_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM users')
            users_count = cursor.fetchone()[0]
            
            conn.close()
            
            await query.edit_message_text(
                f"📊 <b>الإحصائيات</b>\n\n"
                f"🏛️ الجامعات: {unis_count}\n"
                f"📚 المواد: {courses_count}\n"
                f"👥 المستخدمين: {users_count}",
                parse_mode=ParseMode.HTML
            )
        except:
            await query.edit_message_text("❌ خطأ في جلب الإحصائيات")
    
    elif data.startswith("uni:"):
        # عرض مواد الجامعة
        uni_id = int(data.split(":")[1])
        courses = db.get_courses_by_university(uni_id)
        
        if not courses:
            await query.edit_message_text("⚠️ لا توجد مواد في هذه الجامعة")
            return
        
        keyboard = []
        for course_id, code, name, instructor in courses[:10]:
            keyboard.append([InlineKeyboardButton(
                f"📚 {code} - {name}",
                callback_data=f"course:{course_id}"
            )])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back")])
        
        await query.edit_message_text(
            "📚 <b>اختر المادة:</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    
    elif data.startswith("course:"):
        # عرض تفاصيل المادة
        course_id = int(data.split(":")[1])
        
        files = db.get_files_by_course(course_id)
        messages = db.get_messages_by_course(course_id)
        
        text = f"📚 <b>المادة</b>\n\n"
        text += f"📁 الملفات: {len(files)}\n"
        text += f"💌 الرسائل: {len(messages)}\n\n"
        text += f"المحتوى قريباً..."
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back")]]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    
    elif data == "back":
        await query.edit_message_text("🏠 استخدم القائمة الرئيسية")

# ═══════════════════════════════════════════════════════════════════════════
# الخطوة 12: التطبيق الرئيسي
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """التطبيق الرئيسي"""
    print("=" * 70)
    print("🚀 STARTING TELEGRAM BOT - ALL IN ONE")
    print("=" * 70)
    print(f"📁 Database: {DATABASE_PATH}")
    print(f"📝 Log file: {LOG_PATH}")
    print(f"🤖 Bot username: @{BOT_USERNAME}")
    print(f"👑 Admin IDs: {ADMIN_IDS}")
    print("=" * 70)
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ═══════════════════════════════════════════════════════════════════════
    # تسجيل معالجات المحادثة للاستيراد
    # ═══════════════════════════════════════════════════════════════════════
    
    import_conv = ConversationHandler(
        entry_points=[CommandHandler('import', import_command)],
        states={
            IMPORT_TYPE: [CallbackQueryHandler(import_type_selected)],
            IMPORT_FILE: [MessageHandler(filters.Document.ALL, import_file_received)]
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    
    # ═══════════════════════════════════════════════════════════════════════
    # تسجيل جميع المعالجات
    # ═══════════════════════════════════════════════════════════════════════
    
    # معالجات المحادثة
    application.add_handler(import_conv)
    
    # الأوامر الأساسية
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    
    # أوامر الأدمن
    application.add_handler(CommandHandler('adminhelp', adminhelp_command))
    application.add_handler(CommandHandler('stats', stats_command))
    application.add_handler(CommandHandler('listids', listids_command))
    application.add_handler(CommandHandler('adduni', adduni_command))
    application.add_handler(CommandHandler('importunis', importunis_command))
    application.add_handler(CommandHandler('importcourses', importcourses_command))
    
    # معالجات الرسائل والأزرار
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # ═══════════════════════════════════════════════════════════════════════
    # بدء البوت
    # ═══════════════════════════════════════════════════════════════════════
    
    print("✅ BOT IS READY!")
    print("=" * 70)
    print("📱 Open Telegram and search for your bot")
    print("📝 Send /start to begin")
    print("👑 Admin commands: /adminhelp")
    print("=" * 70)
    
    # تشغيل البوت
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# ═══════════════════════════════════════════════════════════════════════════
# نقطة البداية
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # التحقق من التوكن
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ الرجاء تعديل BOT_TOKEN في الملف!")
        print("ابحث عن: YOUR_BOT_TOKEN_HERE")
        print("واستبدله بالتوكن الخاص بك")
        sys.exit(1)
    
    # بدء البوت
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
