"""
#def check_word():
word_in = str(input("Podaj slowo"))
list_in = ['good', 'anna']
list_from_word = sorted(list(word_in))
print(list_from_word)
for n in list_in:
    if sorted(list(n)) in list_from_word:
        print(sorted(list(n)))
        print("true")
    else:
        print("false")
        print(sorted(list(n)))



"""

"""  --- Rozwiazanie 


list_of_words = ['anna', 'good','bad']
input_word = 'bad'

def sort_sup(el: str) -> list:
    return "".join(sorted(el))

final_list_of_words = [sort_sup(el) for el in list_of_words]
def test(input_word: str, list_: list) -> bool:
    return sort_sup(input_word) in list_

test(input_word, final_list_of_words)

"""

"""ZADANKO 2
input_word = 'annabike'
list_of_words = ['anna', 'bike', 'doog', 'lucky']

def combination(list_: str):
    list_ = []
    for n in list_of_words:
        i = [a + n for a in list_of_words]
        list_ = list_ + i
    return list_
def checker(input_word :str, list_: list):
    if input_word in list_
        


"""