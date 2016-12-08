clc
clear all
filename = 'C:\Users\Sam\Desktop\CMPT732\project\gitup\dataset.csv';
M = csvread(filename,1,2)
R = corrcoef(M)