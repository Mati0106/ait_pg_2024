from typing import List


def testForString(testStr: str, testList: List[str]) -> bool:
    newList = testStr.split("")
    #check if any lengths match given word length
    if len(newList) not in [len(item) for item in testList]:
        return False

    #solution form instructor:
    return "".join(sorted(testStr)) in ["".join(sorted(item)) for item in testList]



if __name__ == "__main__":
    test_str: str = "gdoo"
    test_list: List[str] = [
        "anna",
        "good",
        "bike"
    ]
    if testForString(test_str, test_list):
        print(f"{test_str} is in table {test_list}")
    else:
        print(f"{test_str} is NOT in table {test_list}")