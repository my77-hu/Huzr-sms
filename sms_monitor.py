import subprocess
import re
import sqlite3
import os

def get_adb_connection_info():
    """جلب الـ IP والمنفذ النشط للتصحيح اللاسلكي تلقائياً من النظام"""
    try:
        # تنفيذ أمر لجلب حالة اتصالات الـ adb النشطة على الجهاز محلياً
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        output = result.stdout
        
        # البحث عن اتصال لاسلكي قائم
        lines = output.strip().split('\n')
        for line in lines:
            if ':' in line and 'device' in line:
                parts = line.split()[0].split(':')
                return parts[0], int(parts[1])
    except Exception:
        pass
    return None, None

def monitor_sms():
    print("[*] جاري فحص والتحقق من الاتصال اللاسلكي للـ ADB تلقائياً...")
    
    # محاولة إعادة تشغيل الخادم وتفعيل الاتصال المحلي المضمون لاسلكياً
    subprocess.run(['adb', 'start-server'], capture_output=True)
    
    # جلب معلومات الاتصال النشطة
    ip, port = get_adb_connection_info()
    
    if not ip:
        # إذا لم يكن متصلاً، نقوم بالربط التلقائي عبر المنفذ المحلي الافتراضي لاسلكياً
        print("[*] جارٍ تفعيل الجسر اللاسلكي المحلي...")
        subprocess.run(['adb', 'connect', '127.0.0.1:5555'], capture_output=True)
        ip, port = "127.0.0.1", 5555

    print(f"[+] الاتصال اللاسلكي نشط على: {ip}:{port}")
    
    # مسار قاعدة بيانات الرسائل في أندرويد لجميع الشرائح
    sms_paths = [
        "/data/data/com.android.providers.telephony/databases/mmssms.db",
        "/data/user/0/com.android.providers.telephony/databases/mmssms.db"
    ]
    
    success = False
    for sms_path in sms_paths:
        try:
            # استخدام أداة adb لنسخ قاعدة بيانات الرسائل مؤقتاً وقراءتها لاسلكياً
            local_db = "temp_sms.db"
            pull_cmd = f"adb pull {sms_path} {local_db}"
            res = subprocess.run(pull_cmd, shell=True, capture_output=True, text=True)
            
            if res.returncode == 0 and os.path.exists(local_db):
                conn = sqlite3.connect(local_db)
                cursor = conn.cursor()
                
                # جلب الرسائل الواردة لجميع الشرائح (sub_id أو address)
                cursor.execute("SELECT address, body, date, sub_id FROM sms WHERE type=1 ORDER BY date DESC LIMIT 20;")
                messages = cursor.fetchall()
                
                if messages:
                    print(f"\n[+] تم بنجاح سحب رسائل الشرائح لاسلكياً ({len(messages)} رسالة):\n" + "-"*50)
                    for idx, (address, body, date, sub_id) in enumerate(messages, 1):
                        print(f"[{idx}] الشريحة (SIM ID): {sub_id}")
                        print(f"    المرسل: {address}")
                        print(f"    النص: {body}")
                        print("-" * 50)
                    success = True
                conn.close()
                os.remove(local_db)
                break
        except Exception as e:
            continue
            
    if not success:
        print("[-] تعذر سحب قاعدة البيانات مباشرة، تأكد من أن الاتصال اللاسلكي يعمل وصلاحيات التخزين متاحة.")

if __name__ == "__main__":
    monitor_sms()
