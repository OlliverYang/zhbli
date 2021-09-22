function plot_draw_save(num_tracker, plot_style, ave_success_rate_plot, idx_seq_set, rank_num, ...
                        ranking_type, rank_idx, name_tracker_all, threshold_set, title_name, ...
                        x_label_name, y_label_name, fig_name, save_fig_path, save_fig_suf)
% plot and save curves
perf = zeros(1, num_tracker);
for i=1:num_tracker
    %each row is the sr plot of one sequence
    tmp = ave_success_rate_plot(i, idx_seq_set, :);
    aa  = reshape(tmp, [numel(idx_seq_set), size(ave_success_rate_plot, 3)]);
    aa  = aa(sum(aa,2)>eps, :);
    bb  = mean(aa);
    switch ranking_type
        case 'AUC'
            perf(i) = mean(bb);
        case 'threshold'
            perf(i) = bb(rank_idx);
    end
end

[~, index_sort] = sort(perf,'descend');

i = 1;
j = 1;

% plot settings
font_size        = 26; 
% font_size        = 14;
% font_size_legend = 12;   % for overall plot
% font_size_legend = 8;      % for attribute-based plot
font_size_legend = 14;
axex_font_size   = 20;

tmp_figure = figure;
% set(gcf, 'unit', 'normalized', 'position', [0.1,0.1,0.53,0.68]);
%set(gca, 'FontSize', axex_font_size);
set(gcf, 'unit', 'normalized', 'position', [0.1,0.1,0.45,0.77]);      % for overall plot

tmp_axes = axes('Parent', tmp_figure, 'FontSize', axex_font_size);
for k = index_sort(1:rank_num)

    tmp = ave_success_rate_plot(k, idx_seq_set, :);
    aa  = reshape(tmp, [numel(idx_seq_set), size(ave_success_rate_plot, 3)]);
    aa  = aa(sum(aa,2)>eps, :);
    bb  = mean(aa);
    
    switch ranking_type
        case 'AUC'
            score = mean(bb);
            tmp   = sprintf('%.3f', score);
        case 'threshold'
            score = bb(rank_idx);
            tmp   = sprintf('%.3f', score);
    end    
    
    if strcmp(name_tracker_all{k}, 'ECO_HC')
        tmpName{i} = ['ECOhc ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'RLS_ATOM')
        tmpName{i} = ['\bf{RLS-ATOM ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'GD_ATOM')
        tmpName{i} = ['GD-ATOM ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'RLS_DiMP')
        tmpName{i} = ['\bf{RLS-DiMP ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'RLS_DiMPmax')
        tmpName{i} = ['\bf{RLS-DiMPmax ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'GD_DiMP')
        tmpName{i} = ['GD-DiMP ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'DiMP18')
        tmpName{i} = ['DiMP-18 ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'DiMP')
        tmpName{i} = ['DiMP-50 ' '[' tmp ']'];
    else
        tmpName{i} = [name_tracker_all{k} ' [' tmp ']'];
    end
    if strcmp(name_tracker_all{k}, 'ECO_HC') || strcmp(name_tracker_all{k}, 'CSRDCF') || strcmp(name_tracker_all{k}, 'ECO') || strcmp(name_tracker_all{k}, 'SiamFC') || strcmp(name_tracker_all{k}, 'MDNet') || strcmp(name_tracker_all{k}, 'RLS_ATOM') || strcmp(name_tracker_all{k}, 'GD_ATOM') || strcmp(name_tracker_all{k}, 'RLS_DiMP') || strcmp(name_tracker_all{k}, 'RLS_DiMPmax') || strcmp(name_tracker_all{k}, 'GD_DiMP') || strcmp(name_tracker_all{k}, 'DiMP18') || strcmp(name_tracker_all{k}, 'ATOM') || strcmp(name_tracker_all{k}, 'DiMP') || strcmp(name_tracker_all{k}, 'SiamRPN++') || strcmp(name_tracker_all{k}, 'DaSiamRPN') || strcmp(name_tracker_all{k}, 'SiamMask') || strcmp(name_tracker_all{k}, 'LTMU') || strcmp(name_tracker_all{k}, 'DiMP50')
        h(i) = plot(threshold_set, bb, 'color', plot_style{i}.color, 'lineStyle', plot_style{i}.lineStyle,'lineWidth', 3,'Parent', tmp_axes);
        tmpNameplot{j} = tmpName{i};
        hplot(j) = h(i);
        j = j + 1;
    else
        h(i) = plot(threshold_set, bb, 'color', plot_style{i}.color, 'lineStyle', plot_style{i}.lineStyle,'lineWidth', 1.5,'Parent', tmp_axes);
    end
    hold on
%     grid on;
%     if k == index_sort(1)
%         set(gca,'GridLineStyle', ':', 'GridColor', 'k', 'GridAlpha', 1, 'LineWidth', 1.2);
%     end
    i = i + 1;
end
i = 1;
for k = index_sort(1:rank_num)

    tmp = ave_success_rate_plot(k, idx_seq_set, :);
    aa  = reshape(tmp, [numel(idx_seq_set), size(ave_success_rate_plot, 3)]);
    aa  = aa(sum(aa,2)>eps, :);
    bb  = mean(aa);
    
    switch ranking_type
        case 'AUC'
            score = mean(bb);
            tmp   = sprintf('%.3f', score);
        case 'threshold'
            score = bb(rank_idx);
            tmp   = sprintf('%.3f', score);
    end    
    
    if strcmp(name_tracker_all{k}, 'ECO_HC')
        tmpName{i} = ['ECOhc ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'RLS_ATOM')
        tmpName{i} = ['\bf{RLS-ATOM ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'GD_ATOM')
        tmpName{i} = ['GD-ATOM ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'RLS_DiMP')
        tmpName{i} = ['\bf{RLS-DiMP ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'RLS_DiMPmax')
        tmpName{i} = ['\bf{RLS-DiMPmax ' '[' tmp ']}'];
    elseif strcmp(name_tracker_all{k}, 'GD_DiMP')
        tmpName{i} = ['GD-DiMP ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'DiMP18')
        tmpName{i} = ['DiMP-18 ' '[' tmp ']'];
    elseif strcmp(name_tracker_all{k}, 'DiMP')
        tmpName{i} = ['DiMP-50 ' '[' tmp ']'];
    else
        tmpName{i} = [name_tracker_all{k} ' [' tmp ']'];
    end
    if strcmp(name_tracker_all{k}, 'RLS_DiMP')
        h(i) = plot(threshold_set, bb, 'color', plot_style{i}.color, 'lineStyle', plot_style{i}.lineStyle,'lineWidth', 3,'Parent', tmp_axes);
        hold on
    end
%     grid on;
%     if k == index_sort(1)
%         set(gca,'GridLineStyle', ':', 'GridColor', 'k', 'GridAlpha', 1, 'LineWidth', 1.2);
%     end
    i = i + 1;
end
grid on;

if strcmp(ranking_type, 'threshold')
%     legend_position = 'Northwest Outside';  % 'Southeast' or 'Southeastoutside'
    legend_position = 'Southeast';
else
    legend_position = 'Northeast';  % 'Southwest' or 'Southwestoutside'
end
tmpName = tmpName(1:min(end,20));
h = hplot;
hlegend = legend(h, tmpNameplot, 'Interpreter', 'tex', 'fontsize', font_size_legend, 'Location', legend_position);
%hlegend.NumColumns = 2;
title(title_name, 'fontsize', font_size);
xlabel(x_label_name, 'fontsize', font_size);
ylabel(y_label_name, 'fontsize', font_size);
ylim([0 0.85]);
hold off

% save result figures
if ~exist(save_fig_path, 'dir')
    mkdir(save_fig_path);
end
if strcmp(save_fig_suf, 'eps')
    print('-depsc', [save_fig_path fig_name]);
else
    saveas(gcf, [save_fig_path fig_name], 'png');
end

end