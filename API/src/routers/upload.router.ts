/**
 * Required External Modules and Interfaces
 */
 import express, { Request, Response } from "express";
 import { imageFilter } from '../services/utils';
 import { uploadFile, verifyFile } from "../controllers/upload.controller";

/**
 * Router Definition
 */
const multer = require('multer');
const UPLOAD_PATH = 'mnt/Uploads/';
const storage = multer.diskStorage({
    destination: function (req: any, file: any, cb: any) {
      cb(null, `${UPLOAD_PATH}`)
    },
    filename: function (req: any, file: any, cb: any) {
        const date = new Date().getTime();
        const newName = `${date}.mp4`;
        req.params.newName = newName;
      cb(null, newName)
    }
  })

const upload = multer({storage: storage,  fileFilter: imageFilter}); // multer configuration
export const uploadRouter = express.Router();

/**
 * Controller Definitions
 */
uploadRouter.post("/",upload.single('video'), uploadFile );