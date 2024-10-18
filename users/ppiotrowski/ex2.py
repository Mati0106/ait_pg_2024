from typing import List


def isInAnyPair(test: str, inList: List[str]) -> bool:
    for x,y in makePairs(inList):
        if x+y == test or y+x == test:
            return True
    return False

def makePairs(inList:List[str]) -> ():
    it = iter(inList)
    return zip(it, it)


if __name__ == "__main__":
    testInput: str = "annabike"
    testList: List[str] = [
        "anna",
        "karina",
        "bike",
        "whale"
    ]
    for first in testList:
        if testInput.startswith(first):
            for second in testList:
                if first+second == testInput:
                    print("yes")
    print("no")
    #
    # print("-----")
    # print(
    #     "yes" if (isInAnyPair(testInput, testList)) else
    #     "no"
    # )

