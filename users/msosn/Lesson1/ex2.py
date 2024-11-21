import re

list = ["anna", "good", "bike", "annab", "abike"]
word = "annabike"
front_list = []
back_list = []

def match(regex: str, text: str):
    return re.search(regex, text);

for e in list:
    if match(f"^{e}", word):
        front_list.append(e)
    if match(f"{e}$", word):
        back_list.append(e)

print(front_list)
print(back_list)

