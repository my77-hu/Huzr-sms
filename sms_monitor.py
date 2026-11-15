import subprocess

def monitor_sms_direct():
    print("[*] جارٍ فحص مسارات الرسائل عبر الاتصال اللاسلكي...")
    
    # التأكد من عمل الخادم والاتصال اللاسلكي المحلي
    subprocess.run(['adb', 'start-server'], capture_output=True)
    subprocess.run(['adb', 'connect', '127.0.0.1:5555'], capture_output=True)
    
    # قائمة بمسارات محتوى الرسائل المحتملة في أندرويد لجميع الشرائح
    uris = [
        "content://sms/inbox",
        "content://sms",
        "content://telephony/sim/sms"
    ]
    
    success = False
    for uri in uris:
        try:
            cmd = f"adb shell content query --uri {uri}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            
            if output and "No such table" not in output and "Error" not in output and "No result" not in output:
                print(f"\n[+] تم بنجاح جلب الرسائل من المسار: {uri}\n" + "-"*50)
                print(output[:2500])  # طباعة أول جزء من الرسائل بوضوح
                print("-" * 50)
                success = True
                break
        except Exception as e:
            continue
            
    if not success:
        print("[-] تعذر جلب الرسائل عبر محتوى النظام المباشر، جاري محاولة الفحص البديل...")
        # محاولة أخيرة لقراءة قاعدة البيانات مباشرة عبر نسخها المؤقت بمسار بديل
        alt_cmd = "adb shell sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db 'SELECT address, body FROM sms LIMIT 15;'"
        res = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True)
        if res.stdout.strip():
            print(f"\n[+] الرسائل المستخرجة:\n{res.stdout}")
        else:
            print("[-] تأكد من منح الأذونات الكافية أو أن التطبيق يعمل بصلاحيات التصحيح السليم.")

if __name__ == "__main__":
    monitor_sms_direct()
