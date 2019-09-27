
% P300 dataset for eight healthy subjects. This dataset was produced using
% the standard 6x6 Donchin and Farewell P300 Speller Matrix, with an ISI of
% 0.125 ms. There are 7 words with 5 letters each. There are 10 intensification
% sequences per letter. The original procedure used 3 words for training,
% and tried to decode the remaining 4 words for testing.
%
% The most important structure is data.
%
% data.X : EEG Matrix (8 channels)
% data.y : Labels (1/2)
% data.y_stim: Stimulation number: 1-6 rows, 7-12 cols
% data.trial: Sample point where each of the 35 trials starts.
% data.flash: Sample point where each flashing starts (sample point id, duration, stimulation, hit/nohit)

% time between samples: 0.0039 s mostly (determined by looking at
% diff(D.sampleTime))

% Means that we need 154 sample points for 600 ms

%% load data

D = load('P300S08.mat');

%%  Go through 10 sequences of flashes, add the relevant snippets up

trial = 1;

dur = 100;
avg = zeros(12, 8, dur);

istart = 1 + (trial - 1)*120;
istop = 120 + (trial - 1)*120;

for i = istart:istop % got 120 flashes for each letter
    
    t = D.data.flash(i,1);
    c = D.data.flash(i,3);
    
    avg(c,:,:) = squeeze(avg(c,:,:)) + D.data.X(t:t+dur-1,:)';    
end

avg = avg/10;

% Check ground truth
% figure; scatter(D.data.flash(istart:istop,3), D.data.flash(istart:istop,4), 'filled')

%% plot averages for above, single electrode

e = 8;
x = (1:dur)*0.0039;
figure
for c = 1:12
    subplot(12,1,c)
    plot(x,squeeze(avg(c,e,:)))
    ylim([-20, 20])
end


set(gcf, 'Position', [440 56 111 742])

%% plot averages of above, mean over electrodes

figure
for c = 1:12
    subplot(12,1,c)
    plot(x,mean(squeeze(avg(c,6:8,:))))
    ylim([-20, 20])
end

set(gcf, 'Position', [440 56 111 742])

%% try to find p300 form, use all data in one participant

stim_hit = D.data.flash(D.data.flash(:,4) == 2, :);
stim_miss = D.data.flash(D.data.flash(:,4) == 1, :);

d = 153;

figure

for e = 1:8
    
    p300 = [];
    for i = 1:length(stim_hit)
        
        t = stim_hit(i,1);
        p300 = [p300,D.data.X(t:t+d,e)];
        
    end
    
    control = [];
    for i = 1:(length(stim_miss)-1)
        
        t = stim_miss(i,1);
        control = [control,D.data.X(t:t+d,e)];
        
    end
    
    x = (1:154)*0.0039;
    subplot(8,1,e)
    hold on
    plot(x, mean(p300,2))
    plot(x, mean(control,2))
    title(sprintf('Electrode %G', e))
end