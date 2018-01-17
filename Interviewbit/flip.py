class Solution:
    # @param A : string
    # @return a list of integers
    def flip(self, A):
        A=list(A)
        n=len(A)
        L=-1
        for i in range(0,n):
            if(A[i]=='0'):
                L=i
                break
        if(L==-1):
            x=[]
            return x
        x=[-1,-1]
        max=0
        count=0
        R=L
        for i in range(L,n):
            if(A[i]=='0'):
                count+=1
            else:
                count-=1
            if(count>max):
                x=[L,R]
                max=count
            if(count<0):
                count=0
                L=i+1
            R+=1
        if(x[0]==-1):
            x=[]
        else:
            x[0]+=1
            x[1]+=1
        return x

sol = Solution()
A = "0100111000"
print(sol.flip(A))
