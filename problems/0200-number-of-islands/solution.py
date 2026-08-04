"""
200. Number of Islands
Difficulty: Medium
Link: https://leetcode.com/problems/number-of-islands/
"""

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        island=0
        isVisited=set()
        def dfs(r,c):
            if(r not in range(len(grid)) or  c not in range(len(grid[0])) or grid[r][c]=='0' or (r,c) in isVisited ):
                return
            isVisited.add((r,c))
            direct=[[0,1],[1,0],[-1,0],[0,-1]]
            for dr,dc in direct:
                dfs(r+dr,c+dc)
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if(grid[r][c]=="1" and (r,c) not in isVisited):
                    island+=1
                    dfs(r,c)
        return island