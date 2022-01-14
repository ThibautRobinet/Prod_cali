function M = backward(I2,I1,ps, win_s)
   [h0,w0] = size(I1);
    M = zeros(h0/ps,w0/ps,2);
    for k = 1:ps:h0-ps
        for l=1:ps:w0-ps
            block1 = I1(k:(k+ps-1),l:(l+ps-1));
            min = +inf;
            for i = -win_s:win_s
                for j = -win_s:win_s
                    u = k + i;
                    v = k+ps-1+i;
                    w = l+j;
                    z = l+ps-1+j;
                    if (u > 0 && w > 0 && v <= h0 && z <= w0)
                        block2 = I2(u:v,w:z);
                        norme = sum(sum(abs(block2 - block1)));
                        if (norme < min)
                            min = norme;
                            M((k+ps-1)/ps,(l+ps-1)/ps,:) = [i,j];
                        end
                    end
                end
            end
        end
    end
end