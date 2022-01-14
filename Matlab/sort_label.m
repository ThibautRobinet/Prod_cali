function label_file = sort_label(label_file)
    [B, I]= sort(label_file(:,1));
    label_file = label_file(I,:);
end