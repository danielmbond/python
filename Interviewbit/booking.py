def isBalanced(mystring):
    result = mystring.count("(") == mystring.count(")")
    print(result)
    return(result)


isBalanced("a(bcd)d")
isBalanced("(kjds(hfkj)sdhf")
isBalanced("(sfdsf)(fsfsf")
isBalanced("{[]}()")
isBalanced("{[}]")

with open("input.txt", 'r') as f:
    inputArray = []
    for line in f:
        print(line)
        inputArray.append(line.split(","))
    inputArray = sorted(inputArray, key=lambda x: x[1])
    print(inputArray)


def fib(n):
    a, b = 0, 1
    for i in range(n-1):
        a, b = b, a+b
    print(a)
    return a


print(fib(5))


def int2str(numb):
    return str(numb)


print(int2str(1234))
