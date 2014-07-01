%% read logs generated with message_date_logger.py > gmail.txt

    clear all;
    close all;

    data = csvread('gmail.txt');

%% fix date

    fixDate = @(d) datenum(datestr(d/86400 + datenum(1970, 1, 1)));
    
    data = fixDate(data);
    
%% plot it
    
    fig = figure;
    
    hist(data, 41);
    
    L = get(gca,'XLim');
    set(gca,'XTick', linspace(L(1),L(2), 10))
    datetick('x', 12, 'keepticks');
    set(gca,'XMinorTick', 'on', 'YMinorTick', 'on')
    xlabel('date');
    ylabel('# Mails');

    formatDate = @(d) datestr(d, 1);
    title([num2str(length(data)) ' GMail Mails send/received between ' formatDate(min(data)) ' and ' formatDate(max(data))]);

    saveas(fig, 'gmail.png');



