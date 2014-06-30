%% do the parsing
close all;
clear all;

    
dates = getTweetDatesfromJSON('2014-06-30-tweets/data/js/tweet_index.js');


%% plot it
    
    fig = figure;
    
    bar(dates(:, 1), dates(:, 2))
    
    m = mean(dates(:, 2))
    line(xlim, [m, m]);
    
    L = get(gca,'XLim');
    set(gca,'XTick', linspace(L(1),L(2), 10))
    datetick('x', 12, 'keepticks');
    set(gca,'XMinorTick','on','YMinorTick','on')
    xlabel('date');
    ylabel('# tweets');
    
    formatDate = @(d) datestr(d, 1);
    title([num2str(sum(dates(:, 2))) ' Tweets send between ' formatDate(min(dates(:, 1))) ' and ' formatDate(max(dates(:, 1)))]);

    saveas(fig, 'tweets.png');
    
    