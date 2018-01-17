class Solution:
    # @param A : list of integers
    # @param B : list of integers
    # @return an integer
    def coverPoints(self, X, Y):
        x1 = X[0]
        y1 = Y[0]
        i = 1
        distance = 0
        while i < len(X):
            dx = abs(X[i] - x1)
            dy = abs(Y[i] - y1)
            distance += min(dx, dy) + abs(dx-dy)
            x1 = X[i]
            y1 = Y[i]
            i += 1
        return distance

            
A = [-7, -13]
B = [1, -5]

sol = Solution()
print(sol.coverPoints(A, B))
