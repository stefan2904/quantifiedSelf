function [ dates, datesReceived ] = getSMSfromXML( filename )
%GETSMSFROMXML Summary of this function goes here
%   Detailed explanation goes here

    fprintf('parse sms from %s ... \n', filename);

    xDoc = xmlread(filename);
    
    xRoot = xDoc.getDocumentElement;

    smses = xRoot.getChildNodes;

    if ~smses.hasChildNodes
        error('No SMSes found?');
    end;

    num = smses.getLength;

    dates = zeros(num, 1);
    datesReceived = zeros(num, 1);
    smsID = 0;  % needed, because not every sms node is valid

    tic;
    for i = 1:num;
        sms = smses.item(i-1);
        if sms.hasAttributes
            theAttributes = sms.getAttributes;
            %numAttributes = theAttributes.getLength;
            
            smsID = smsID + 1;
            
            % type = 1; % 2 = send, 1 = received
            type = str2double(theAttributes.getNamedItem('type').getValue);
            date = str2double(theAttributes.getNamedItem('date').getValue);
            if type == 2;
                dates(smsID) = date;
            else
                datesReceived(smsID) = date;
            end;
        end;
    end;
    toc;
    
    dates = dates(dates~=0);
    datesReceived = datesReceived(datesReceived~=0);
    
    earliest = min([min(dates), min(datesReceived)]);
    last = max([max(dates), max(datesReceived)]);
    formatDate = @(d) datestr(d/86400000 + datenum(1970,1,1), 1);
    fprintf('Send %d and received %d SMS between %s and %s!\n\n', length(dates), length(datesReceived), formatDate(earliest), formatDate(last));
        
end

