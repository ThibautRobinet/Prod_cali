/**
 * Required External Modules and Interfaces
 */

 import express, { Request, Response } from "express";

/**
 * Router Definition
 */
 export const pingRouter = express.Router();
/**
 * Controller Definitions
 */

// GET Ping

pingRouter.get("/ping", async (req: Request, res: Response) => {
    try {
      const ping = "Pong";
      res.status(200).send(ping);
    } catch (e: any) {
      res.status(500).send(e.message);
    }
  });
  
  // GET version
  
  pingRouter.get("/version", async (req: Request, res: Response) => {
    try {
      const version = "1.0.0";
      res.status(200).send(version);
    } catch (e: any) {
      res.status(500).send(e.message);
    }
  });
