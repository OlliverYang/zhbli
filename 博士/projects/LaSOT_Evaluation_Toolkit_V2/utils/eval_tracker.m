function eval_tracker(seqs, trackers, eval_type, name_tracker_all, tmp_mat_path, path_anno, rp_all, norm_dst)
% evaluate each tracker
num_tracker = numel(trackers);

threshold_set_overlap = 0:0.01:1;
threshold_set_error   = 0:50;
if norm_dst
    threshold_set_error = threshold_set_error / 100;
end

for i = 1:numel(seqs) % for each sequence
    s    = seqs{i};      % name of sequence
    
    % load GT and the absent flags
    anno        = dlmread([path_anno s '.txt']);
    absent_anno = dlmread([path_anno 'absent/' s '.txt']);
    
    for k = 1:num_tracker  % evaluate each tracker
        t = trackers{k};   % name of tracker
        if (strcmp(t.name, 'ATOM') || strcmp(t.name, 'DiMP18') || strcmp(t.name, 'DiMP'))
            idxNum = 5;
        elseif (strcmp(t.name, 'RLS_ATOM') || strcmp(t.name, 'GD_ATOM') || strcmp(t.name, 'RLS_DiMP') || strcmp(t.name, 'GD_DiMP')) || strcmp(t.name,'DiMP50')
            idxNum = 20;
        else
            idxNum = 1;
        end
        len_all = 0;
        % load tracking result
        % res = dlmread([rp_all t.name '_tracking_result/' s '.txt']);
%         res = load([rp_all t.name '_tracking_result/' s '.txt']);
%         results = load([rp_all t.name '_tracking_result/' s '.txt']);
%         results = load([rp_all s '_' t.name '.mat']);
%         results = results.results;
        fprintf(['evaluating ' t.name ' on ' s ' ...\n']);
        
%         anno     = rect_anno;
        
        success_num_overlap = zeros(idxNum, numel(threshold_set_overlap));
        success_num_err     = zeros(idxNum, numel(threshold_set_error));
        
%         res = results{1};
        for idx = 1:idxNum
            if strcmp(t.name, 'ATOM')
                res = dlmread([rp_all t.name '_tracking_result/default_' num2str(idx-1,'%03d') '/' s '.txt']);
            elseif strcmp(t.name, 'DiMP18')
                res = dlmread([rp_all t.name '_tracking_result/dimp18_' num2str(idx-1,'%03d') '/' s '.txt']);
            elseif strcmp(t.name, 'DiMP50')
                res = dlmread([rp_all t.name '_tracking_result/dimp50_' num2str(idx-1,'%03d') '/' s '.txt']);
            elseif strcmp(t.name, 'DiMP')
                res = dlmread([rp_all t.name '50_tracking_result/dimp50_' num2str(idx-1,'%03d') '/' s '.txt']);
            elseif (strcmp(t.name, 'RLS_ATOM') || strcmp(t.name, 'GD_ATOM') || strcmp(t.name, 'RLS_DiMP') || strcmp(t.name, 'GD_DiMP'))
                res = dlmread([rp_all t.name '_tracking_result/' s '-' num2str(idx-1) '.txt']);
            elseif strcmp(t.name, 'RLS_DiMPmax')
                res = dlmread([rp_all t.name '_tracking_result/' s '-5.txt']);
            else
                res = dlmread([rp_all t.name '_tracking_result/' s '.txt']);
            end
            if isempty(res)
                break;
            end

            [err_coverage, err_center] = calc_seq_err_robust(res, anno, absent_anno, norm_dst);

            for t_idx = 1:numel(threshold_set_overlap)
                success_num_overlap(idx, t_idx) = sum(err_coverage > threshold_set_overlap(t_idx));
            end

            for t_idx = 1:length(threshold_set_error)
                success_num_err(idx, t_idx) = sum(err_center <= threshold_set_error(t_idx));
            end

            len_all = len_all + size(anno, 1);  % number of frames in the sequence
        end
        if (strcmp(t.name, 'ATOM') || strcmp(t.name, 'DiMP18') || strcmp(t.name, 'DiMP') || strcmp(t.name, 'RLS_ATOM') || strcmp(t.name, 'GD_ATOM') || strcmp(t.name, 'RLS_DiMP') || strcmp(t.name, 'GD_DiMP')) || strcmp(t.name, 'DiMP50')
            ave_success_rate_plot(k, i, :)     = sum(success_num_overlap)/(len_all + eps);
            ave_success_rate_plot_err(k, i, :) = sum(success_num_err)/(len_all + eps);
        else
            ave_success_rate_plot(k, i, :)     = success_num_overlap/(len_all + eps);
            ave_success_rate_plot_err(k, i, :) = success_num_err/(len_all + eps);
        end
    end
end

% save results
if ~exist(tmp_mat_path, 'dir')
    mkdir(tmp_mat_path);
end

dataName1 = [tmp_mat_path 'aveSuccessRatePlot_' num2str(num_tracker) 'alg_overlap_' eval_type '.mat'];
save(dataName1, 'ave_success_rate_plot', 'name_tracker_all');

dataName2 = [tmp_mat_path 'aveSuccessRatePlot_' num2str(num_tracker) 'alg_error_' eval_type '.mat'];
ave_success_rate_plot = ave_success_rate_plot_err;
save(dataName2, 'ave_success_rate_plot', 'name_tracker_all');

end