import collections

a = collections.Counter("abcdabcd")
b = collections.Counter("abcdabcd")
c = collections.Counter("abcdabcd")

print(a + b)
print(sum([a, b, c]))