function [ dates ] = getTweetDatesfromJSON( filename )

    fprintf('parse Tweets from %s ... \n', filename);

    data = fileread(filename);
    data = strrep(data, sprintf('var tweet_index =  '), '');
    data = strrep(data, sprintf(' '), '');
    months = parse_json(data);
    
    months = months{1};
    
    dates = zeros(length(months), 2);
    
    for i = 1:length(months);
        month = months{i};
        fprintf('%d-%2d: %4d tweets \n', month.year, month.month, month.tweet_count);
        dates(i, 1) = datenum(datestr([month.year, month.month, 1, 00, 00, 00]));
        dates(i, 2) = month.tweet_count;
    end;

%     earliest = min([min(dates), min(datesReceived)]);
%     last = max([max(dates), max(datesReceived)]);
%     formatDate = @(d) datestr(d/86400000 + datenum(1970,1,1), 1);
%     fprintf('Send %d and received %d Teets between %s and %s!\n\n', length(dates), length(datesReceived), formatDate(earliest), formatDate(last));
        
end

