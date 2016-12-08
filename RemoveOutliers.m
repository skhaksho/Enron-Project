clc
clear all
% read the data and save in a matrix
filename = 'C:\Users\Sam\Desktop\CMPT732\project\gitup\dataset.csv';
M = csvread(filename,1,2);
[M1,M_names,M2]=xlsread(filename,'B:B');
[M1,M_col,M2]=xlsread(filename,'A1:W1');
N=M_names(1);
M_names=M_names(2:end);
%M_names={'','',};
% number of features and poi

fearures_n=size(M(1,:))+1;
poi_0=0;
poi_1=0;
size=size(M);
for i=1:size(:,1)
if M(i,14)==0
    poi_0=poi_0+1;
else 
    poi_1=poi_1+1;
end
end


% outliers for bonus
[bonus,Index]=sort(M(:,1),'descend');
top5_bonus=bonus(1:5)
top5_index=M_names(Index(1:5))
M(Index(1:5),14) % poi or not

% removing TOTAL as it is an outlier
M_f=M(1:130,:);
M_l=M(132:end,:);
M=[M_f;M_l];
M_names=[M_names(1:130);M_names(132:end)];

%outliers for exercised_stock_options
[stock,Index2]=sort(M(:,6),'descend');
top5_stock=stock(1:5)
top5_index2=M_names(Index2(1:5))
M(Index2(1:5),14) % poi or not

%outliers for loan_advances
[loan,Index3]=sort(M(:,11),'descend');
top5_loan=loan(1:5)
top5_index3=M_names(Index3(1:5))
M(Index3(1:5),14) % poi or not

%outliers for others
[others,Index4]=sort(M(:,13),'descend');
top5_others=others(1:5)
top5_index4=M_names(Index4(1:5))
M(Index4(1:5),14) % poi or not

%outliers for restricted_stock
[restricted,Index5]=sort(M(:,15),'descend');
top5_restricted=restricted(1:5)
top5_index5=M_names(Index5(1:5))
M(Index5(1:5),14) % poi or not

%outliers for restricted_stock_deferred
[deferred,Index6]=sort(M(:,16),'descend');
top5_deferred=deferred(1:5);
top5_index6=M_names(Index6(1:5))
M(Index6(1:5),14) % poi or not

%Checking if the feature values are correct?
%Salary+bonus++direct_fees+deferral_payment+deffered_income++loan_advencs+long_term_oincetive+expenses+other=total
%payment
M_totalPayment=M(:,17)+M(:,4)+M(:,2)+M(:,3)+M(:,11)+M(:,12)+M(:,7)+M(:,13)+M(:,1);

%restrickted_stock+exercised_stock_options+restrickted_stock_deferred=total_stock_value
M_stock=M(:,15)+M(:,6)+M(:,16);

for i=1:145
if M_totalPayment(i)~=M(i,20)
    i;
    M_names(i);

end
if M_stock(i)~=M(i,21)
    i;
    M_names(i);
end
end
% change the values related to BELFER ROBERT and BHATNAGAR SANJAY.
% Corrected values are brought from enron61702insiderpay.pdf
%BELFER ROBERT
M(9,3)=-102500;
M(9,2)=0;
M(9,7)=3285;
M(9,4)= 102500;
M(9,20)= 3285;
M(9,6)= 0;
M(9,15)=44093;
M(9,16)= -44093;
M(9,21)= 0;
%BHATNAGAR SANJAY
M(12,13)=0;
M(12,7)=137864;
M(12,4)=0;
M(12,20)= 137864;
M(12,6)= 15456290;
M(12,15)= 2604490;
M(12,16)=-2604490;
M(12,21)=15456290;
%rechecking
M_totalPayment=M(:,17)+M(:,4)+M(:,2)+M(:,3)+M(:,11)+M(:,12)+M(:,7)+M(:,13)+M(:,1);

%restrickted_stock+exercised_stock_options+restrickted_stock_deferred=total_stock_value
M_stock=M(:,15)+M(:,6)+M(:,16);

for i=1:145
if M_totalPayment(i)~=M(i,20)
    i
    M_names(i)

end
if M_stock(i)~=M(i,21)
    i
    M_names(i)
end
end
% Table1=M(:,1:13);
% Table2=M(:,15:end);
% Table=[Table1,Table2];

newDataset='C:\Users\Sam\Desktop\CMPT732\project\gitup\newDataset.xls';
f5=horzcat(M_names,num2cell(M));
f6=vertcat(M_col,f5);
xlswrite(newDataset,f6);