from functions.write_files import write_file

def show(title, text):
    print(title)
    
    if text.startswith("Error:"):
        print(f"    {text}\n")
    else:
        print(text if text.endswith("\n") else text + "\n")

if __name__ == "__main__":
    r1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    show('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):', r1)

    r2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    show('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):', r2)

    r3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    show('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):', r3)
    