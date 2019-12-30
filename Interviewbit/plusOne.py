class Solution:
    # @param A : list of integers
    # @return a list of integers
    def plusOne(self, A):
        num = ""
        total = 0
        result = []
        for i in A:
            num += str(i)
        total = int(num) + 1

        for i in list(str(total)):
            result.append(i)
        return result


A = [1, 2, 3]
sol = Solution()
sol.plusOne(A)
