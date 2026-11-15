import subprocess
import json
import time

# قائمة الهواتف المراقبة
PHONES = [
    {"name": "هاتف_تجربة_1", "ip": "10.179.39.245:5555"},
]

def get_phone_sms(device_ip):
    try:
        # الاتصال بالهاتف لاسلكياً عبر adb
        subprocess.run(["adb", "connect", device_ip], capture_output=True, timeout=5)
        
        # تنفيذ أمر قراءة صندوق الوارد (SMS Inbox) مباشرة من أندرويد
        cmd = ["adb", "-s", device_ip, "shell", "content query --uri content://sms/inbox --projection address:body:date"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        output = result.stdout
        messages = []
        
        for line in output.splitlines():
            if "Row:" in line or "address=" in line:
                messages.append(line)
                
        return messages
    except Exception as e:
        print(f"[-] فشل الاتصال بالهاتف {device_ip}: {e}")
        return []

def main():
    print("[+] بدء المراقبة المركزية للشرائح عن بُعد...")
    seen_messages = set()

    while True:
        for phone in PHONES:
            print(f"[*] جاري فحص: {phone['name']} ({phone['ip']})")
            sms_list = get_phone_sms(phone['ip'])
            
            for sms in sms_list:
                if sms not in seen_messages:
                    seen_messages.add(sms)
                    print(f"\n[!] رسالة جديدة على [{phone['name']}]:\n{sms}\n" + "-"*40)
                    
        time.sleep(5)  # الفحص كل 5 ثوانٍ

if __name__ == "__main__":
    main()
