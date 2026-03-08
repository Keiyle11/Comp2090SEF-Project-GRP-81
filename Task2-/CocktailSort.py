# -*- coding: utf-8 -*-
def cocktailSort(a):
    Length = len(a)
    swapped = True
    start = 0
    end = Length-1
    while (swapped == True):

        swapped = False
        for i in range(start, end):
            if (a[i] > a[i + 1]):
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if (swapped == False):
            break
        swapped = False
        end = end-1
        for i in range(end-1, start-1, -1):
            if (a[i] > a[i + 1]):
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        start = start + 1

a = [4,6,1,8,9,2,9,10]
cocktailSort(a)
print("Sorted array is:")
for i in range(len(a)):
    print("% d" % a[i])