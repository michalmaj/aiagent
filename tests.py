from functions.run_python_files import run_python_file

def show(title, text):
    print(title)
    
    if text.startswith("Error:"):
        print(f"    {text}\n")
    else:
        print(text if text.endswith("\n") else text + "\n")

if __name__ == "__main__":
    r1 = run_python_file("calculator", "main.py")
    show('run_python_file("calculator", "main.py"):', r1)

    r2 = run_python_file("calculator", "main.py", ["3 + 5"])
    show('run_python_file("calculator", "main.py", ["3 + 5"]):', r2)

    r3 = run_python_file("calculator", "tests.py")
    show('run_python_file("calculator", "tests.py"):', r3)

    r4 = run_python_file("calculator", "../main.py")
    show('run_python_file("calculator", "../main.py"):', r4)

    r5 = run_python_file("calculator", "nonexistent.py")
    show('run_python_file("calculator", "nonexistent.py"):', r5)
