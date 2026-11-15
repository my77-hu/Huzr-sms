import subprocess

def monitor_sms_via_content():
    print("[*] جاري الاتصال اللاسلكي وفحص الرسائل عبر موفر محتوى أندرويد...")
    
    # التأكد من تفعيل الاتصال اللاسلكي المحلي
    subprocess.run(['adb', 'start-server'], capture_output=True)
    subprocess.run(['adb', 'connect', '127.0.0.1:5555'], capture_output=True)
    
    try:
        # استخدام أمر adb shell لجلب الرسائل الواردة مباشرة من محتوى النظام (يعمل لاسلكياً وبدون روت)
        cmd = "adb shell content query --uri content://sms/inbox --projection address:body:date:sub_id"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip()
        if not output or "No such table" in output or "Error" in output:
            print("[-] لم يتم العثور على رسائل أو أن الاستعلام يحتاج لتعديل المسار.")
            return

        print(f"\n[+] تم بنجاح سحب رسائل الشرائح لاسلكياً:\n" + "-"*50)
        
        # تحليل النتائج وطباعتها بوضوح
        rows = output.split("Row:")
        for idx, row in enumerate(rows[1:], 1):
            print(f"[{idx}] البيانات: {row.strip().replace(';', ' | ')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"[-] حدث خطأ أثناء التنفيذ: {e}")

if __name__ == "__main__":
    monitor_sms_via_content()
