import fs from 'fs';

/**
 * Service Methods
 */
const videoFolder = '/mnt/Uploads/';
const resultFolder = '/mnt/Results/';
 
 export const isFileExist = (id: string): Boolean => {
    const filePath = videoFolder + id + '.mp4';
    let result = false;
    if (fs.existsSync(filePath)) {
        // File exists in path
        result = true;
      } else {
        // File doesn't exist in path
        result = false;
      }
    return result;
 };
 export const isResultExist = (id: string): Boolean => {
    const filePath = resultFolder + id + '.json';
    let result = false;
    if (fs.existsSync(filePath)) {
        // File exists in path
        result = true;
      } else {
        // File doesn't exist in path
        result = false;
      }
    console.log(result,filePath);
    return result;
 };

 export const getResultJson = (id: string): any => {
    const filePath = resultFolder + id + '.json';
    let file = JSON.parse(fs.readFileSync(filePath,'utf8'));
    console.log(file);
    return file;
 };