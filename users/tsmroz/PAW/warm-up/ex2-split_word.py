def check(input_word: str, lista: list) -> bool:
    # Check parts of word are in a list
    for i in range(len(input_word)):
        a, b = input_word[:i], input_word[i:]
        if (a in lista) and (b in lista):
            return True
    return False

# Run and check function
lista=['anna', 'brzoza', 'krowa', 'jablko']
print(check('annajablko', lista))
print(check('annatom', lista))