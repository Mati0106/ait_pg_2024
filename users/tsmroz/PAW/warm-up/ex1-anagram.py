def count_letters(a: str) -> dict:
    # Create dictionary and count letters
    dict_1 = {}
    for letter in a:
        if letter in dict_1:
            dict_1[letter] += 1
        else:
            dict_1[letter] = 1
    return dict_1


def is_anagram(a: str, b: str) -> bool:
    # Check if letters in a are in b and make anagram
    dict_1 = count_letters(a)
    dict_2 = count_letters(b)
    for key1, value1 in dict_1.items():
        if key1 not in dict_2.keys():
            return False
        if dict_1[key1] > dict_2[key1]:
            return False
    return True


def check_anagram_in_list(a: str, list: list) -> bool:
    # Go through the list and check anagrams
    count = 0
    for b in list:
        if is_anagram(a, b):
            count += 1
    return count > 0


# Run and check functions
list_1 = ['anna', 'brzoza', 'krowa', 'jablko']

print(check_anagram_in_list("rzaob", list_1))
print(check_anagram_in_list("rziob", list_1))