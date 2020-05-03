#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:46:22 2020

@author: amith
"""

class PartialMatch:
    
    def __init__(self, lhs_string= '', rhs_string= ''):
        self.lhs_string = self.rhs_string = None
        self.set_lhs_string(lhs_string)
        self.set_rhs_string(rhs_string)
    
    def set_lhs_string(self, lhs_string):
        """
        If rhs_string is constant and only lhs_string changes, use this function 
        to set lhs string instead of creating a new object of the class. Saves up
        time taken to process rhs_string
        """
        if lhs_string is self.lhs_string:
            return
        self.lhs_string = lhs_string
        self.matching_substrings = None
        
    def set_rhs_string(self, rhs_string):
        if rhs_string is self.rhs_string:
            return
        self.rhs_string = rhs_string
        self.matching_substrings = None
        self.__hash_rhs_string()
        
    def __hash_rhs_string(self):
        """
        rhs_string_hash[character] is a list of indices(sorted ascending) of the occurences of the
        character in rhs_string.
        eg. {'a': [1,3,8,10], 'm': [....], .....}
        Use set_rhs_string() to avoid this loop running again and again
        """
        rhs_string = self.rhs_string
        
        self.rhs_string_hash = rhs_string_hash = {}
        
        for i, char in enumerate(rhs_string):
            indices = rhs_string_hash.setdefault(char, [])
            indices.append(i)
        
    # Closing for import. Not handling out of bound errors since it's not needed
    # for internal use     
    def __find_longest_substring(self, lhs_low, lhs_high, rhs_low, rhs_high):t
        """
        Input parameters are upper and lower bounds of lhs and rhs string. Function
        returns the longest matching substring in lhs_string[lhs_low:lhs_high] and 
        rhs_string[rhs_low:rhs_high]
        
        Output is a match tuple (i,j,k) 
        i - start index in lhs_string
        j - start index in rhs_string
        k - length
        longest matched substring - lhs_string[i:i+k] or rhs_string[j:j+k] 
        """
        lhs_string, rhs_string_hash = self.lhs_string, self.rhs_string_hash
        
        besti, bestj, bestsize = None, None, 0
        
        # j2len[j] = length of longest substring
        j2len = {}
        for i in range(lhs_low, lhs_high):
            temp_j2len = {}
            for j in rhs_string_hash.get(lhs_string[i], []):
                if j < rhs_low:
                    continue
                if j >= rhs_high:
                    break
                k = temp_j2len[j] = j2len.get(j-1, 0) + 1
                if k > bestsize:
                    besti, bestj, bestsize = i-k+1, j-k+1, k
            j2len = temp_j2len

        return (besti, bestj, bestsize)
    
    def get_matching_substrings(self):
        """
        Returns a list of match tuples (i,j,k) of all matches in decreasing order of
        size of the substring
        """
        if self.matching_substrings is not None:
            return self.matching_substrings
        
        lhs_string_len, rhs_string_len = len(self.lhs_string), len(self.rhs_string)
        
        next_input_list = [(0, lhs_string_len, 0, rhs_string_len)] # Base condition
        
        matching_substrings = []
        while next_input_list:
            lhs_low, lhs_high, rhs_low, rhs_high = next_input_list.pop()
            i, j, k = self.__find_longest_substring(lhs_low, lhs_high, rhs_low, rhs_high)
            
            if k:
                matching_substrings.append((i, j, k))
                if lhs_low < i and rhs_low < j:
                    # left side of the matched substring
                    next_input_list.append((lhs_low, i, rhs_low, j)) 
                if i+k < lhs_high and j+k < rhs_high:
                    # right side of the matched substring
                    next_input_list.append((i+k, lhs_high, j+k, rhs_high))
        
        self.matching_substrings = matching_substrings
        
        return self.matching_substrings
    
    def calculate_absolute_ratio(self):
        matches = sum(match_tuple[-1] for match_tuple in self.get_matching_substrings())
        combined_length = len(self.lhs_string) + len(self.rhs_string)
        if combined_length:
            return 2*matches/combined_length
        return 1
    
    def calculate_partial_ratio(self):
        """
        Calculating ratio in extended vicinity of each block and taking avg 
        of ratios of all blocks. 
        """
        lhs_string_len = len(self.lhs_string)        
        rhs_string_len = len(self.rhs_string)

        if lhs_string_len > rhs_string_len:
            long_string = self.lhs_string
            short_string = self.rhs_string
        else:
            long_string = self.rhs_string
            short_string = self.lhs_string
            
        ratio_arr = []
        for substring in self.get_matching_substrings():
            long_start = substring[1] - substring[0]
            if long_start < 0:
                long_start = 0 
            long_end = substring[1] + len(short_string)
            block_ratio = substring[2]/len(long_string[long_start:long_end])
            ratio_arr.append(block_ratio)
        return sum(ratio_arr)/len(ratio_arr)
            
            
    
                
            
        
        
        
        
        
        
        