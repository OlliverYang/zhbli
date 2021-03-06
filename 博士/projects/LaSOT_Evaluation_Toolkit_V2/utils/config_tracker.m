function trackers = config_tracker()
% config trackers to be evaluated
% note: the evaluation under protocol 1 (i.e., all 1,400 videos) for newly
% added 13 trackers are not available. Thus, you may need to comment these
% 13 trackers (ATOM, DiMP, C-RPN, SiamRPN++, DaSiamRPN, D-STRCF, SiamDW, GFSDCF, 
% SiamMask, GlobalTrack, SPLT, ASRCF, LTMU) when performing evaluation using 
% all 1,400 videos.
trackers = {struct('name', 'DiMP50',      'publish', 'ICCV-19')};
end