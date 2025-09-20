from functions.get_files_info import get_files_info

def print_result(title, result):
    print(f"{title}")
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.splitlines():
            print(f" {line}")
    print() 

if __name__ == "__main__":
    res1 = get_files_info("calculator", ".")
    print_result('get_files_info("calculator", "."):\nResult for current directory:', res1)

    res2 = get_files_info("calculator", "pkg")
    print_result("get_files_info(\"calculator\", \"pkg\"):\nResult for 'pkg' directory:", res2)

    res3 = get_files_info("calculator", "/bin")
    print_result("get_files_info(\"calculator\", \"/bin\"):\nResult for '/bin' directory:", res3)

    res4 = get_files_info("calculator", "../")
    print_result("get_files_info(\"calculator\", \"../\"):\nResult for '../' directory:", res4)