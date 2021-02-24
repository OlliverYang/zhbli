clear;clc;
path1 = '.\PTAV';
filelist = dir(path1); %序列名
[n,c] =size(filelist); %返回矩阵行,列，n为序列总数
disp(n);disp(c);
 for i = 3:n;
     disp(filelist(i).name);
     Newname=strcat(filelist(i).name(1:end-4),'_PTAV.mat'); %Basketball_ltdsst
     matrix1 = importdata(fullfile(path1,filelist(i).name));
     shape = size(matrix1);
     len = shape(1);
     s1 = struct('res',{matrix1},'len',len, 'type','rect');
     results={s1};
     save(fullfile(path1,Newname),'results');
%      disp(newname);
 end