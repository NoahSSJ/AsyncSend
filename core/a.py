import re
pattern = r"\w+"
tests = ["hello", "123", "user_1", "hello-world"]

for t in tests:
    match = re.search(pattern, t)
    if match:
        print(match.group(0))
    else:
        print("no match")