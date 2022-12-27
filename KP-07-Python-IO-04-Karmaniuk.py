from Control import run
#запускаємо
namem = input("write file title\n(введіть назву файла Коду С в форматі .txt)\n")
with open('KP-07-Python-IO-04-Karmaniuk.asm', 'w') as f:
    pass

with open(namem, 'rb') as f:
    c_file = f.read().decode('utf-8')
print("KP-07-Python-IO-04-Karmaniuk.txt:")
print(c_file)

asm_code, error = run(c_file)

if error:
    print('Error: ' + error.as_string())
else:
    print("\nKP-07-Python-IO-04-Karmaniuk.asm")
    print(asm_code)
    print('\nProcess finished successfully')
    with open('KP-07-Python-IO-04-Karmaniuk.asm', 'w') as f:
        f.write(asm_code)

input()