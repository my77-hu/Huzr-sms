import subprocess

def monitor_sms_final():
    print("[*] جاري الاتصال اللاسلكي وسحب رسائل الشرائح...")
    
    # تفعيل الاتصال اللاسلكي المحلي
    subprocess.run(['adb', 'start-server'], capture_output=True)
    subprocess.run(['adb', 'connect', '127.0.0.1:5555'], capture_output=True)
    
    try:
        # أمر استعلام مباشر من قاعدة بيانات رسائل أندرويد الداخلية مع تحديد رقم الشريحة (sub_id) والمنصات
        cmd = "adb shell sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db 'SELECT sub_id, address, body, date FROM sms ORDER BY date DESC LIMIT 20;'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip()
        if not output:
            print("[-] لم يتم إرجاع بيانات، جاري محاولة مسار بديل...")
            # مسار بديل لقاعدة البيانات في بعض إصدارات أندرويد
            alt_cmd = "adb shell sqlite3 /data/user/0/com.android.providers.telephony/databases/mmssms.db 'SELECT sub_id, address, body, date FROM sms ORDER BY date DESC LIMIT 20;'"
            result = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()

        if output:
            print(f"\n[+] تم بنجاح سحب رسائل الشرائح لاسلكياً:\n" + "-"*50)
            lines = output.split('\n')
            for idx, line in enumerate(lines, 1):
                print(f"[{idx}] {line.replace('|', ' | الشريحة/النص: ')}")
                print("-" * 50)
        else:
            print("[-] تعذر سحب البيانات، تأكد أن وضع التصحيح اللاسلكي نشط تماماً.")
            
    except Exception as e:
        print(f"[-] حدث خطأ: {e}")

if __name__ == "__main__":
    monitor_sms_final()
