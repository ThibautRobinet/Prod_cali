/**
 * Data Model Interfaces
 */
 const fs = require('fs');
/**
 * Service Methods
 */
 
 export const writeCommandFile = (fileName: string) => {
  const video_path = "/mnt/Uploads/"+fileName;
  const images_path = "/mnt/Images/" + fileName.replace('.mp4','');
  const res_path = "/mnt/Results/" + fileName.replace('.mp4','');
  const command_path = "/mnt/Commands/file2process.txt";

  fs.appendFile(command_path, video_path +'\n'+images_path+'\n'+res_path+'\n', function (err :any) {
    if (err) throw err;
    console.log('Added to file2process.txt !');
 });
 };