function d = make_table()

dur = 100;

d = table();

for i = 1:8
    
    d_temp = table();
    
    D = load(sprintf('P300S0%G.mat',1));
    
    n = size(D.data.flash,1);
    
    d_temp.time = nan(n,1);
    d_temp.stim = nan(n,1);
    d_temp.hit = nan(n,1);
    
    d_temp.e1 = nan(n,dur);
    d_temp.e2 = nan(n,dur);
    d_temp.e3 = nan(n,dur);
    d_temp.e4 = nan(n,dur);
    d_temp.e5 = nan(n,dur);
    d_temp.e6 = nan(n,dur);
    d_temp.e7 = nan(n,dur);
    d_temp.e8 = nan(n,dur);
    
    d_temp.ID = ones(n,1)*i;
    
    for j = 1:n
        
        pointid = D.data.flash(j,1);
        
        d_temp.time(j) = D.sampleTime(pointid);
        d_temp.stim(j) = D.data.flash(j,3);
        d_temp.hit(j) = D.data.flash(j,4);
        
        d_temp.e1(j,:) = D.data.X(pointid:pointid+dur-1,1);
        d_temp.e2(j,:) = D.data.X(pointid:pointid+dur-1,2);
        d_temp.e3(j,:) = D.data.X(pointid:pointid+dur-1,3);
        d_temp.e4(j,:) = D.data.X(pointid:pointid+dur-1,4);
        d_temp.e5(j,:) = D.data.X(pointid:pointid+dur-1,5);
        d_temp.e6(j,:) = D.data.X(pointid:pointid+dur-1,6);
        d_temp.e7(j,:) = D.data.X(pointid:pointid+dur-1,7);
        d_temp.e8(j,:) = D.data.X(pointid:pointid+dur-1,8);
    end
    
    d = [d; d_temp];
end

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    