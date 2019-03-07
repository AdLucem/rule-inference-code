

def is_same_sentence(a, b):
    
def is_same(a, b):
    _a = a.encode("utf-8", "ignore")
    _b = b.encode("utf-8", "ignore")

    return (_a == _b)


def is_same_test():

    s1 = "cat"
    s2 = "bat"
    s3 = "cat"

    print(is_same(s1, s2))
    print(is_same(s2, s3))
    print(is_same(s1, s3))


def is_same_sentence_test():

    test_l = ["this is a cat",
              "this is the bat",
              "this is the cat",
              "this is the bat"]

    for i in test_l:
        for j in test_l:



if __name__ == "__main__":

    is_same_test()
