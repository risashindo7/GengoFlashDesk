# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:52:23 2017

@author: Risa
"""

path = 'retrieval/data/data_french/CARDIMG.ALL'
pathdest = 'retrieval/data/data_french/CARDIMGCopy.ALL'
 
with open(path, 'r') as file1:
    with open(pathdest, 'w') as file2:
        for line in file1:
            if ".I" in line:
                file2.write(line)
            elif ".W" in line:
                file2.write(line)
            else:
                splitlist = line.split(' - ')
                #index = line.index( ' ', line.index( ' ' ) + 1 )
                #firstChunk = line[0:index]
                firstChunk = splitlist[0]
                #secondChunk = line.substr( index + 1 )
                file2.write(firstChunk + " - ;\n")