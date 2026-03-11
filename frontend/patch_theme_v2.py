import glob
import os

files = ['index.html', 'login.html', 'signup.html']

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if file == 'index.html':
        content = content.replace('--primary-green: #87A330;', '--primary-green: #5A9367;')
        content = content.replace('--dark-green: #243010;', '--dark-green: #3F4B3B;')
        content = content.replace('--light-green: #A1C349;', '--light-green: #5CAB7D;')
        content = content.replace('--soft-bg: #CAD593;', '--soft-bg: #F4F7F5;')

    if file in ['login.html', 'signup.html']:
        content = content.replace('background-color: #CAD593;', 'background-color: #F4F7F5;')
        content = content.replace('color: #243010;', 'color: #3F4B3B;')
        content = content.replace('background: #87A330;', 'background: #5A9367;')
        content = content.replace('background: #A1C349;', 'background: #5CAB7D;')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Landing & Auth themes updated successfully.")
