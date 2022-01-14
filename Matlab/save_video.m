video = VideoWriter('film.mp4'); %create the video object
open(video); %open the file for writing
for k=200:299 %where N is the number of images
  name = sprintf('img_%02d.jpg',k);
  I = imread(name); %read the next image
  writeVideo(video,I); %write the image to file
end
close(video); %close the file