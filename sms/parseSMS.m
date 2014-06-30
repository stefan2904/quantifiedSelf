%% do the parsing
close all;
clear all;

    
    [dates1, dates1received] = getSMSfromXML('sms-2011-0917-222402.xml');
    [dates2, dates2received] = getSMSfromXML('sms-2014-05-18 06-26-27.xml');

%% do the date conversion
    
    dates = [dates1; dates2];
    datesReceived = [dates1received; dates2received];

    unixtime2date = @(d) datenum(datestr(d/86400000 + datenum(1970,1,1)));

    datestrs = unixtime2date(dates);
    datestrsReceived = unixtime2date(datesReceived);

%% plot it
    
    figSend = figure;
    hist(datestrs, 36);
    datetick('x', 12, 'keepticks');
    xlabel('date');
    ylabel('# sms');
    
    formatDate = @(d) datestr(d/86400000 + datenum(1970,1,1), 1);
    title(['SMS send between ' formatDate(min(dates)) ' and ' formatDate(max(dates))]);
    
    saveas(figSend, 'sms_send.png');
    
    figRec = figure;
    hist(datestrsReceived, 36);
    datetick('x', 12, 'keepticks');
    xlabel('date');
    ylabel('# sms');
    
    title(['SMS received between ' formatDate(min(datesReceived)) ' and ' formatDate(max(datesReceived))]);
    
    saveas(figRec, 'sms_received.png');
    
    