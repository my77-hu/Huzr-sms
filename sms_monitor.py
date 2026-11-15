import subprocess
import json

# عنوان الهاتف الذي حددناه
PHONES = [
    {"name": "هاتف_تجربة_1", "ip": "10.179.39.245:5555"},
]

def get_phone_sms(device_ip):
    try:
        print(f"[*] جاري الاتصال بالهاتف وجلب الرسائل المخزنة من: {device_ip}")
        # الاتصال بالهاتف لاسلكياً عبر adb
        subprocess.run(["adb", "connect", device_ip], capture_output=True, timeout=5)
        
        # تنفيذ أمر قراءة صندوق الوارد (SMS Inbox) بالكامل للرسائل السابقة
        cmd = ["adb", "-s", device_ip, "shell", "content query --uri content://sms/inbox --projection address:body:date"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        output = result.stdout
        messages = []
        
        for line in output.splitlines():
            if "Row:" in line or "address=" in line or "body=" in line:
                messages.append(line)
                
        return messages
    except Exception as e:
        print(f"[-] فشل الاتصال بالهاتف {device_ip}: {e}")
        return []

def main():
    print("[+] بدء جلب الرسائل النصية القديمة المخزنة على الأجهزة...\n")
    
    for phone in PHONES:
        sms_list = get_phone_sms(phone['ip'])
        
        if sms_list:
            print(f"\n[+] تم بنجاح العثور على {len(sms_list)} سجل/رسالة في هاتفك:")
            for sms in sms_list:
                print(f"  {sms}")
        else:
            print(f"[-] لم يتم العثور على رسائل أو تعذر الاتصال بـ {phone['name']}.")

if __name__ == "__main__":
    main()
