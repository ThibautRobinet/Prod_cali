clear all
close all
clc 

%% Partie 3 %%
%Paths
root_path = '/Users/thibaut/Desktop/Projet_Cali/Dataset';
video_folder = 'Videos_MERL_Shopping_Dataset';
%Choose video
SubjectID = 1;
sessionID = 1;
% Create name
video_name = sprintf('%d_%d_crop',SubjectID,sessionID);
video_full_name = sprintf('%s/%s/%s.mp4',root_path,video_folder,video_name);
% Load video
video = VideoReader(video_full_name);

%% Extract images
for k = 200:299
    img = double(rgb2gray(read(video,k)));
    img2 = double(rgb2gray(read(video,k+3)));
    %img3 = double(rgb2gray(read(video,k+6)));

    % figure;
    % subplot 131, imshow(uint8(img));
    % subplot 132, imshow(uint8(img2));
    % subplot 133, imshow(uint8(img3));

    %% Find mouvment vectors
    pas = 8;
    [h,w] = size(img);
    v = backward(img2,img,pas,7);

    i = flowToColor(v);
    i2 = imresize(i,pas);

    vi = v(:,:,1);
    vj = v(:,:,2);
    vj2 = vj;
    for i = 1:h/pas;
        vj2(i,:) = -vj(h/pas +1 - i,:);
    end
    % figure
    % subplot 221, imshow(uint8(img));
    % subplot 222,quiver(vi,vj);
    % subplot 223, imshow(i2);
    % subplot 224,quiver(vi,vj2);

    %% new image
    img = imresize(img,[85,115]);
    image = zeros(85,115,3);
    image(:,:,1) = img;
    image(:,:,2) = vi;
    image(:,:,3) = vj2;
    name = sprintf('img_%02d.jpg',k);
    imwrite(image,name);
end
%figure, imagesc(image);
