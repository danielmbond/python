# Definition for an interval.
# class Interval:
#     def __init__(self, s=0, e=0):
#         self.start = s
#         self.end = e


class Solution:
    # @param intervals, a list of Intervals
    # @param newInterval, a Interval
    # @return a list of Interval
    def insert(self, intervals, newInterval):
        res = []
        if len(intervals) == 0:
            res.append(newInterval)
            return res
        # insert the new interval
        intervals.append(newInterval)
        # sort list according to the start value
        intervals.sort(key=lambda x: x.start)

        res.append(intervals[0])
        # scan the list
        for i in range(1, len(intervals)):
            cur = intervals[i]
            pre = res[-1]
            # check if current interval intersects with previous one
            if cur.start <= pre.end:
                res[-1].end = max(pre.end, cur.end)  # merge
            else:
                res.append(cur)  # insert

        return res
