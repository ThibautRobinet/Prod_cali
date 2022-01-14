function label = get_label(label_file,framePos)
       I = find(label_file(:,1) <= framePos & label_file(:,2) > framePos );
       label = label_file(I,3);
       if (length(label)==0)
           label = 0;
       end
end