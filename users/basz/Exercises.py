# Sprawdź wyraz w liście
def can(word, dictionary):
    for y in dictionary:
        if all(word.count(char) <= y.count(char) for char in word):
            return True
    return False


dictionary = ["dom", "drop", "anna", "telefon"]
word = "mod")
if can(word, dictionary):
    print( word +" może")
else:
    print(word +" nie może")

# Czy można ułożyć słowo z połączenia dwóch słów z listy
def can(word, dictionary):
    for i in range(len(dictionary)):
        for j in range(len(dictionary)):
            if i != j:  
                if word == dictionary[i] + dictionary[j]:
                    return True
    return False


dictionary = ["anna", "nana", "dom", "samochód", "komputer"]
word = "annana"

if can(word, dictionary):
    print( word +" może")
else:
    print(word +" nie może")