
import base64
import os

def get_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

agents_b64 = get_b64(r'c:\Users\jeena\Downloads\jaaf-framework-main\jaaf-framework-main\core\agents.py')
bot_b64 = get_b64(r'c:\Users\jeena\Downloads\jaaf-framework-main\jaaf-framework-main\telegram_bot.py')

with open('upload_script.sh', 'w') as f:
    f.write(f"echo '{agents_b64}' | base64 -d > core/agents.py\n")
    f.write(f"echo '{bot_b64}' | base64 -d > telegram_bot.py\n")
    f.write("npx pm2 restart all\n")

print("Generated upload_script.sh")
