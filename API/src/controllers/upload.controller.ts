import express, { Request, Response } from "express";
import { writeCommandFile } from "../services/upload.service";

export const uploadFile =  async (req: Request, res: Response) => {
    try {
        console.log(req.params.validate)
        if (!req.params.validate){
            res.status(500).send('File not received');
            console.log(`No File received as avatar form-data field`);
        }
        else if (req.params && req.params.file_error) {
            res.status(500).send(req.params.file_error);
            console.log(`Wrong extension`);
        }
        else{
            console.log(`Video saved`);
            writeCommandFile(req.params.newName)
            let response = {message: `Video saved : ${req.params.newName}`,newName : `${req.params.newName}`};

            res.status(200).send(response);
        }
    } catch (e : any) {
        console.log(`Error`);
        res.status(500).send(e.message);
    }
};

export const verifyFile =  (req: Request, res: Response) => {
    console.log(req.params)
};