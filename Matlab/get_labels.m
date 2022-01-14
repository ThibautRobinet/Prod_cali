function [X] = get_labels(label_name)
    load(label_name)

    X = [];
    for i = 1:5
        Y = tlabs{i};
        Z = i*ones(size(Y,1),1);
        X = [X;  [Y Z] ];
    end
end