class Solution:

    def maxSubArray(self,ls):
        if len(ls) == 0:
           raise Exception("Array empty") # should be non-empty
          
        runSum = maxSum = ls[0]
        i = 0
        start = finish = 0

        for j in range(1, len(ls)):
            if ls[j] > (runSum + ls[j]):
                runSum = ls[j]
                i = j
            else:
                runSum += ls[j]

            if runSum > maxSum:
                maxSum = runSum
                start = i
                finish = j

        print ("maxSum =>", maxSum)
        print ("start =>", start, "; finish =>", finish)
        return maxSum

test = Solution()
#print(test.maxSubArray((1,2,3,4)))

A = (-2,1,-3,4,-1,2,1,-5,4)
##A = (-163, -20)
print(test.maxSubArray(A))
