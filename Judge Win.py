# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:21:06 2020

@author: 15495
"""

def Judge(x,y,color,CHESSLOCATION):#x,y是当前落子的坐标，color保存当前落子颜色，CHESSLOCATION是棋盘数组
    count1,count2,count3,count4=0,0,0,0#四个变量分别保存四个方向相同颜色棋子数目 
    #横向判断
    i=x-1
    while(i>=0):    
        if color==CHESSLOCATION[i][y]:
            count1+=1
            i=i-1
        else:
            break
    i=x+1
    while i<15: 
        if CHESSLOCATION[i][y]==color:
            count1+=1
            i=i+1
        else:
            break
    
    #纵向判断
    j=y-1
    while(j>=0):
        if color==CHESSLOCATION[x][j]:
            count2+=1
            j=j-1
        else:
            break
    j=y+1
    while j<15:
        if CHESSLOCATION[x][j]==color:
            count2+=1
            j=j+1
        else:
            break
        
    #正对角线判断
    i=x-1
    j=y-1
    while(i>=0 and j>=0):
        if color==CHESSLOCATION[i][j]:
            count3+=1
            i=i-1
            j=j-1
        else:
            break
    i=x+1
    j=y+1
    while (i<15 and j<15):
        if CHESSLOCATION[i][j]==color:
            count3+=1
            i=i+1
            j=j+1 
        else:
            break
        
    #反对角线判断
    i=x+1
    j=y-1
    while(i<15 and j>=0):
        if color==CHESSLOCATION[i][j]:
            count4+=1
            i=i+1
            j=j-1
        else:
            break
    i=x-1
    j=y+1
    
    while (i>0 and j<15):
        if CHESSLOCATION[i][j]==color:
            count4+=1
            i=i-1
            j=j+1
        else:
            break
    
    if count1==5 or count2==5 or count3==5 or count4==5:
        return True
    else:
        return False
    