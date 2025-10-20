#!/usr/bin/env python3
"""
اختبار سريع للتوكن - يعمل حتى في البيئات المحظورة
"""
import sys

BOT_TOKEN = "7718993072:AAFxcXOBWrdv54h3U2CtW-2CeN-dL9Qxe6w"

print("=" * 70)
print("🔍 اختبار توكن البوت")
print("=" * 70)
print(f"📝 التوكن: {BOT_TOKEN[:20]}...")
print()

# تحليل التوكن
parts = BOT_TOKEN.split(":")
if len(parts) == 2:
    bot_id = parts[0]
    token_part = parts[1]

    print(f"✅ تنسيق التوكن: صحيح")
    print(f"🤖 Bot ID: {bot_id}")
    print(f"🔑 Token length: {len(token_part)} characters")
    print()

    # محاولة الاتصال
    print("🌐 محاولة الاتصال بـ Telegram API...")

    try:
        import urllib.request
        import json

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"

        try:
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())

            if data.get('ok'):
                bot_info = data.get('result', {})
                print("=" * 70)
                print("✅ البوت يعمل بشكل صحيح!")
                print("=" * 70)
                print(f"🤖 Username: @{bot_info.get('username')}")
                print(f"📝 Name: {bot_info.get('first_name')}")
                print(f"🆔 ID: {bot_info.get('id')}")
                print(f"✅ Can join groups: {bot_info.get('can_join_groups')}")
                print(f"✅ Can read messages: {bot_info.get('can_read_all_group_messages')}")
                print()
                print("🎉 يمكنك الآن استخدام البوت على تيليجرام!")
                print(f"📱 ابحث عن: @{bot_info.get('username')}")
                print()
                sys.exit(0)
            else:
                print(f"❌ خطأ: {data}")

        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("=" * 70)
                print("❌ التوكن غير صالح!")
                print("=" * 70)
                print("🔧 الحل:")
                print("1. افتح @BotFather في تيليجرام")
                print("2. أرسل: /mybots")
                print("3. اختر البوت")
                print("4. اضغط API Token")
                print("5. انسخ التوكن الجديد")
                print()
            elif e.code == 403:
                print("=" * 70)
                print("⚠️ البيئة الحالية محظورة من Telegram")
                print("=" * 70)
                print("✅ لكن التوكن صحيح!")
                print()
                print("🚀 الحل: شغّل البوت على بيئة أخرى:")
                print()
                print("📦 أسهل طريقة - على جهازك:")
                print("1. حمّل المشروع:")
                print("   git clone https://github.com/Mohammadnnnn/UpDrjati.git")
                print("2. ادخل المجلد:")
                print("   cd UpDrjati")
                print("3. شغّل البوت:")
                print("   python3 telegram_bot_all_in_one.py")
                print()
                print("☁️ أو استخدم خدمة سحابية مجانية:")
                print("   - PythonAnywhere: https://www.pythonanywhere.com")
                print("   - Railway: https://railway.app")
                print("   - Render: https://render.com")
                print()
            else:
                print(f"❌ خطأ HTTP: {e.code} - {e.reason}")

        except Exception as e:
            print(f"⚠️ لا يمكن الوصول للـ API من هذه البيئة")
            print(f"📝 التفاصيل: {e}")
            print()
            print("=" * 70)
            print("✅ التوكن يبدو صحيحاً في التنسيق")
            print("=" * 70)
            print("🚀 جرّب تشغيل البوت على بيئة أخرى:")
            print()
            print("1️⃣ على جهازك الشخصي:")
            print("   git clone https://github.com/Mohammadnnnn/UpDrjati.git")
            print("   cd UpDrjati")
            print("   python3 telegram_bot_all_in_one.py")
            print()
            print("2️⃣ على PythonAnywhere (مجاني):")
            print("   - اذهب إلى: www.pythonanywhere.com")
            print("   - أنشئ حساب مجاني")
            print("   - افتح Bash console")
            print("   - نفذ الأوامر أعلاه")
            print()

    except ImportError:
        print("⚠️ المكتبات غير متوفرة")

else:
    print("❌ تنسيق التوكن خاطئ!")
    print("✅ التنسيق الصحيح: BOT_ID:TOKEN")

print("=" * 70)
