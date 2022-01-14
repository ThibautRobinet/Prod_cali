/**
 * Required External Modules and Interfaces
 */

 import express, { Request, Response } from "express";

 import { getResult } from "../controllers/result.controller";


export const resultRouter = express.Router();

/**
 * Controller Definitions
 */

resultRouter.get("/:id",getResult);