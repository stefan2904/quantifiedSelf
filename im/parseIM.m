%% read adium logs generated with export_adium.py --onlydate

    clear all;
    close all;

    data = csvread('adium.csv', 1, 0);

%% fix date

    fixDate = @(d) datenum(datestr(d/86400 + datenum(1970, 1, 1)));
    
    data = fixDate(data);
    
%% plot it
    
    fig = figure;
    
    hist(data, 68);
    
    L = get(gca,'XLim');
    set(gca,'XTick', linspace(L(1),L(2), 10))
    datetick('x', 12, 'keepticks');
    set(gca,'XMinorTick', 'on', 'YMinorTick', 'on')
    xlabel('date');
    ylabel('# IMs');

    formatDate = @(d) datestr(d, 1);
    title([num2str(length(data)) ' IMs send/received between ' formatDate(min(data)) ' and ' formatDate(max(data))]);

    saveas(fig, 'im.png');



