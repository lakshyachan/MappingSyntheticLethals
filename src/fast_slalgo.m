addpath('/data/lakshmi/FastSL-master/Genes');                            
addpath('/data/lakshmi/cobratoolbox');
addpath('/data/lakshmi');
initCobraToolbox
%solverOK = changeCobraSolver('ibm_cplex');
folder = '/data/lakshmi/mat/';
file_list = dir(fullfile(folder,'*.mat'));
problem_orgs = {};
for k = 2:length(file_list)
   tic
   orgname = file_list(k).name;
   load(orgname);
   toc
   try 
       solution = optimizeCbModel(model);
       maxGrowth(k,1) = solution.f; 
       mkdir('/data/lakshmi/results'); 
       tic
       [sgd,dgd,tgd] = fastSL_tg(model,0.01,1);
       toc
       tic 
       orgname = strrep(orgname,'.mat','');
       sgdpath = strcat('/data/lakshmi/results/',orgname,'_sgd.csv');
       dgdpath = strcat('/data/lakshmi/results/',orgname,'_dgd.csv');
       tgdpath = strcat('/data/lakshmi/results/',orgname,'_tgd.csv');
       toc
       cell2csv(sgdpath,sgd);
       cell2csv(dgdpath,dgd);
       cell2csv(tgdpath,tgd);
       disp(k);
   catch 
       problem_orgs = [problem_orgs, orgname];
   end       
   cell2csv('/data/lakshmi/problem_orgs.csv',problem_orgs);
end
fprintf('\n Finished Fast-SL on all 818 organisms of AGORA...');
