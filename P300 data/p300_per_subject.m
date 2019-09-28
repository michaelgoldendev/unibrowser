function p300_per_subject(d)

figure

for sub = unique(d.ID)'
    
    subplot(3,8,sub)
    hold on
    plot(mean(d.e6(d.hit == 1 & d.ID == sub,:)))
    plot(mean(d.e6(d.hit == 2 & d.ID == sub,:)))
    title(sprintf('Sub %G, Electrode %G', sub, 6))    
end

for sub = unique(d.ID)'
    
    subplot(3,8,sub + 8)
    hold on
    plot(mean(d.e7(d.hit == 1 & d.ID == sub,:)))
    plot(mean(d.e7(d.hit == 2 & d.ID == sub,:)))
    title(sprintf('Sub %G, Electrode %G', sub, 7))    
end

for sub = unique(d.ID)'
    
    subplot(3,8,sub + 16)
    hold on
    plot(mean(d.e8(d.hit == 1 & d.ID == sub,:)))
    plot(mean(d.e8(d.hit == 2 & d.ID == sub,:)))
    title(sprintf('Sub %G, Electrode %G', sub, 8))    
end

end