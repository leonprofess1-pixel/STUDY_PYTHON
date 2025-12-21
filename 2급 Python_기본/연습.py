
arr = [4,2,1,3,9,5,6]

for i in range(7):
    a=i
    for j in range(i,7):
        if arr[j]<arr[a]:
                a=j     
    arr[i], arr[a] = arr[a], arr[i]

print(arr)

