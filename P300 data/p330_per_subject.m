function p330_per_subject(d)

figure

for sub = unique(d.ID)'
    
    subplot(1,8,sub)
    hold on
    plot(mean(d.e1(d.hit == 1 & d.ID == sub,:)))
    plot(mean(d.e1(d.hit == 2 & d.ID == sub,:)))
    title(sprintf('Sub %G, Electrode %G', sub, 8))    
end
end