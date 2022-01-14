function [] = prepare_video(video_path,dest_folder)
    warning('off', 'MATLAB:MKDIR:DirectoryExists');
    if (isfile(video_path))
        % Load video
        video = VideoReader(video_path);
        % Compute size
        video_size = floor(video.NumFrames/12)*12;

        % Create video thum folder
        list_img_name = 'list_img.txt';
        mkdir(dest_folder);
        list_img_path = sprintf('%s/%s',dest_folder, list_img_name);
        fid=fopen(list_img_path,'a');

        %% Create Frames 
        for k = 1:12:video_size % On en prend une frame sur 2 pour passer de 30fps à 15fps puis une frame sur 6
            frameID = ceil(k/2);
            %% Extract frame
            img = read(video,k);

            %% Save frame
            frame_name = sprintf('%s/thumb-%03d_2.jpg',dest_folder,frameID);
            imwrite(img,frame_name);
            fprintf(fid, [frame_name '\n']);% Save frame name
        end
        fclose(fid);
    end
end