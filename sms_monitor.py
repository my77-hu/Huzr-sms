import subprocess

def monitor_sms_content_provider():
    print("[*] جاري الاتصال اللاسلكي وسحب رسائل الشرائح عبر موفر محتوى النظام...")
    
    # تفعيل خادم الاتصال والربط لاسلكياً محلياً
    subprocess.run(['adb', 'start-server'], capture_output=True)
    subprocess.run(['adb', 'connect', '127.0.0.1:5555'], capture_output=True)
    
    try:
        # استخدام أمر content query لجلب رسائل الصندوق الوارد متضمنة رقم الشريحة (sub_id) والمرسل والنص
        cmd = "adb shell content query --uri content://sms/inbox --projection sub_id:address:body:date"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip()
        
        if not output or "No such table" in output or "Error" in output:
            # محاولة مسار بديل إذا لم يستجب المسار الأول
            alt_cmd = "adb shell content query --uri content://sms --projection sub_id:address:body:date"
            result = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()

        if output and "Row:" in output:
            print(f"\n[+] تم بنجاح سحب رسائل الشرائح لاسلكياً:\n" + "-"*50)
            rows = output.split("Row:")
            for idx, row in enumerate(rows[1:], 1):
                clean_row = row.strip().replace(", ", "\n    ").replace("=", ": ")
                print(f"[{idx}] تفاصيل الرسالة:\n    {clean_row}")
                print("-" * 50)
        else:
            print("[-] لم يتم العثور على رسائل واردة، أو أن الصندوق فارغ حالياً.")
            
    except Exception as e:
        print(f"[-] حدث خطأ أثناء السحب: {e}")

if __name__ == "__main__":
    monitor_sms_content_provider()
