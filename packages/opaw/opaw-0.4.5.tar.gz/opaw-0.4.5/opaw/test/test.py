def p15552():
    import sys
    read = sys.stdin.readline
    n = int(read().strip())

    for _ in range(n):
        a, b = map(int, read().strip().split())
        print(a + b)


def p11021():
    n = int(input())

    for i in range(n):
        a, b = map(int, input().split())
        print(f"Case #{i + 1}: {a + b}")


def p10951():
    while True:
        try:
            a, b = map(int, input().split())
            print(a + b)
        except Exception:
            break


def p10807():
    """
    11
    1 4 1 2 4 2 4 2 3 4 4
    2
    """
    input()
    nums = list(map(int, input().split()))
    target = int(input())
    print(nums.count(target))


def p5597():
    import sys
    r = sys.stdin.read().split()
    absent = []
    for i in range(1, 31):
        if str(i) not in r:
            absent.append(str(i))
    print(" ".join(absent))


def p1546():
    input()
    scores = list(map(int, input().split()))
    max_s = max(scores)
    new_s = 0
    for s in scores:
        new_s += s / max_s * 100
    print(round(new_s / len(scores), 2))


def p9086():
    n, *l = [*open(0)]
    for s in l:
        s=s.strip()
        print(s[0]+s[-1])
    for _ in range(int(input())):
        s = input()
        print(s[0] + s[-1])

def p11718():
    print(f'''{sys.stdio.read()}''')

# p9086()

a2d = {
    "ABC": 2,
    "DEF": 3,
    "GHI": 4,
    "JKL": 5,
    "MNO": 6,
    "PQRS": 7,
    "TUV": 8,
    "WXYZ": 9,
}

t = 0
for a in "UNUCIC":
    for k,v in a2d.items():
        if a in k:
            t += v+1

print(t)



