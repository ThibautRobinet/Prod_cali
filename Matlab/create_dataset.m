clear all;
close all;
warning('off', 'MATLAB:MKDIR:DirectoryExists');

%% Initialisation 
%Folders 
video_folder = 'Videos_MERL_Shopping_Dataset';
labels_folder = 'Labels_MERL_Shopping_Dataset';
list_folder = 'merlTrainTestList';
image_folders = {'train','validation','test'};%'Images_MERL_Shopping_Dataset';

%Files
label_file = 'classInd.txt';
train_file = 'trainlist01.txt'; % videos 1->20
validation_file = 'validationlist01.txt';% videos 21->26
test_file = 'testlist01.txt'; % videos 27->41


for SubjectID = 33:41
    for sessionID = 1:3
        
        fprintf('Video %d:%d \n',SubjectID,sessionID)
        %Values
        type = 1;
        if (SubjectID >= 27)
            type = 3;
        elseif (SubjectID >= 21)
            type = 2;
        end
        image_folder = image_folders{type};

        %Paths
        root_path = '/Users/thibaut/Desktop/Projet_Cali/Dataset';
        frame_path = sprintf('%s/%s',root_path,image_folder);

        %% Load video
        % Create name
        video_name = sprintf('%d_%d_crop',SubjectID,sessionID);
        video_full_name = sprintf('%s/%s/%s.mp4',root_path,video_folder,video_name);
        
        if (isfile(video_full_name))
            % Load video
            video = VideoReader(video_full_name);
            % Compute size
            video_size = floor(video.NumFrames/12)*12;


            %% Folders and file processing
            % Create video thum folder
            video_crop_folder = sprintf('%s/%s',frame_path,video_name);
            mkdir(video_crop_folder);
            % Open label index folder
            list_label_file_name = sprintf('%s/%s/%s',root_path, list_folder, label_file);
            fid=fopen(list_label_file_name,'a');

        %% Load labels
        % Create name
        label_name = sprintf('%d_%d_label.mat',SubjectID,sessionID);
        label_path = sprintf('%s/%s/%s',root_path,labels_folder,label_name);
        % Load video
        labels = get_labels(label_path);
        labels = sort_label(labels);

            %% Create Frames 
            for k = 1:12:video_size % On en prend une frame sur 2 pour passer de 30fps à 15fps puis une frame sur 6
                frameID = ceil(k/2);
                %% Extract frame
                img = read(video,k);

                %% Save frame
                frame_name = sprintf('%s/thumb-%03d_2.jpg',video_name,frameID);
                imwrite(img,fullfile(frame_path,frame_name));

                %% Get frame label
                frame_label = get_label(labels,k);

                %% Save label
                for i = 1:length(frame_label)
                    frame_line = sprintf('%s %d\n',frame_name,frame_label(i));
                    fprintf(fid, frame_line);
                end
            end
            fclose(fid);

            %% Add to list
            %Values
            list_file_name = sprintf('%s/%s/%s',root_path, list_folder, train_file);
            if (type == 2)
                list_file_name = sprintf('%s/%s/%s',root_path, list_folder, validation_file);
            elseif (type == 3)
                list_file_name = sprintf('%s/%s/%s',root_path, list_folder, test_file);
            end

            fid=fopen(list_file_name,'a');
            fprintf(fid, video_name);
            fprintf(fid, '\n');
            fclose(fid);
        end
    end
end