from functions.get_file_content import get_file_content

def show(title, text):
    print(title)
    # jeśli Error, zrób wcięcie jak w przykładach z poprzedniego zadania
    if text.startswith("Error:"):
        print(f"    {text}\n")
    else:
        print(text if text.endswith("\n") else text + "\n")

if __name__ == "__main__":
    r1 = get_file_content("calculator", "main.py")
    show('get_file_content("calculator", "main.py"):', r1)

    r2 = get_file_content("calculator", "pkg/calculator.py")
    show('get_file_content("calculator", "pkg/calculator.py"):', r2)

    r3 = get_file_content("calculator", "/bin/cat")
    show('get_file_content("calculator", "/bin/cat"):', r3)

    r4 = get_file_content("calculator", "pkg/does_not_exist.py")
    show('get_file_content("calculator", "pkg/does_not_exist.py"):', r4)