import sys
class Solution:
    # @param A : list of integers
    # @return an integer
    # |A[i] - A[j]| + |i - j|
    def maxArr(self, A):
        result = 0
        ans = max1 = max2 = max3 = max4 = (-sys.maxsize - 1)
        
        for i in range(len(A)):
            print("max1",max1,"max2",max2,"max3",max3,"max4",max4,"ai",A[i],"i",i)
            max1 = max(max1,A[i] +i)
            max2 = max(max2,-A[i] +i)
            max3 = max(max3,A[i] -i)
            max4 = max(max4,-A[i] -i)
            print(ans)
            ans=max(ans,max1-A[i]-i);
            print(ans)
            ans=max(ans,max2+A[i]-i);
            print(ans)
            ans=max(ans,max3-A[i]+i);
            print(ans)
            ans=max(ans,max4+A[i]+i);
            print(ans)

        return(ans)

sol = Solution()
A = [1, 3, -1]
#A = [2, 2, 2]
print(sol.maxArr(A))
