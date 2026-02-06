from functions.get_file_content import get_file_content
from config import MAX_CHARS

# lorem truncation test

truncated_read = get_file_content("calculator", "lorem.txt")
if len(truncated_read) > MAX_CHARS:
    print(f"truncation active, size is: {len(truncated_read)}")
    print("checking for truncation message...")
    truncation_message = truncated_read[MAX_CHARS:]
    print(truncation_message)

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))