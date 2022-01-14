import { NextFunction,Request, Response } from "express";
import { isFileExist, isResultExist, getResultJson } from "../services/result.service";


export const getResult =  async (req: Request, res: Response, next : NextFunction) => {
    try {
        if(!req.params || !req.params.id){
            res.status(500).send('INVALID params: require videoID');
        }
        else{
            if (isFileExist(req.params.id)){
                if (isResultExist(req.params.id)){
                    
                    let file  = getResultJson(req.params.id);
                    let response = {status: "Terminated", result:file.result};
                    res.status(200).send(response);
                }
                else{
                    let response = {status: "Processing data"};
                    res.status(200).send(response);
                }
            }
            else{
                let response = {status: "File does not exist"};
                res.status(200).send(response);
            }  
        }
    } catch (e : any) {
        console.log(`Error`);
        res.status(500).send(e.message);
    }
};

export const verifyFile =  (req: Request, res: Response) => {
    console.log(req.params)
};