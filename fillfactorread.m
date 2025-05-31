% 讀取 Excel 資料
data = readtable('Lissajous_Fill_Factor_PerPhase.xlsx');

% 變數名稱
names = data.Properties.VariableNames;

% 取得 Combined 欄位名稱
combined_col = names{contains(names, 'Combined', 'IgnoreCase', true)};

% 嚴格抓 Phase0 ~ Phase7（剛好 8 個）
phase_cols = {};
for i = 0:7
    pat = sprintf('Phase%d', i);
    idx = find(contains(names, pat) & contains(names, 'Fill'), 1);
    if ~isempty(idx)
        phase_cols{end+1} = names{idx};
    end
end

% Phase 對應的角度標籤
phase_labels = {'0', 'π/4', 'π/2', '3π/4', 'π', '5π/4', '3π/2', '7π/4'};

% 讀取對應資料
x = data.x;
ratio = data.ratio;
combined = data.(combined_col);

% 顏色
colors = lines(8);

% 畫圖
figure;
hold on;

for i = 1:8
    y = data.(phase_cols{i});
    plot(x, y, '-o', 'DisplayName', sprintf('Phase %d (%s)', i-1, phase_labels{i}), ...
        'Color', colors(i, :));
end

% 畫粉紅色的 Combined 線
plot(x, combined, '-s', 'LineWidth', 2, 'Color', [0, 0, 0], ...
    'DisplayName', 'Combined 8 Phases');

% 加上 ratio 標註（frame rate）
for i = 1:length(x)
    text(x(i), combined(i) + 1.5, sprintf('%d Hz', ratio(i)), ...
        'FontSize', 9, 'HorizontalAlignment', 'center', 'Color', 'b');
end

% 標籤與格式
xlabel('x (fx = ratio * x, fy = ratio * (x - 1))');
ylabel('Fill Factor (%)');
title('Lissajous Fill Factor per Phase with Frame Rate (ratio)');
legend('Location', 'southeastoutside');
grid on;
ylim([0 80]);
xlim([0 38]);
hold off;
