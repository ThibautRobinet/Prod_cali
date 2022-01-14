/**
 * Required External Modules
 */

import * as dotenv from "dotenv";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { pingRouter } from "./routers/ping.router";
import { uploadRouter } from "./routers/upload.router";
import { resultRouter } from "./routers/result.router"
import { errorHandler } from "./middleware/error.middleware";
import { notFoundHandler } from "./middleware/not-found.middleware";
import swaggerUi from 'swagger-ui-express';
const pathToSwaggerUi = require('swagger-ui-dist').absolutePath()
const swaggerDocument = require('../openapi.json');


 
dotenv.config();
/**
 * App Variables
 */

 if (!process.env.PORT) {
    process.exit(1);
 }
 
 const PORT: number = parseInt(process.env.PORT as string, 10);
 
 const app = express();
/**
 *  App Configuration
 */
 app.use('/documentation', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
 app.use(helmet());
 app.use(cors());
 app.use(express.json());
 app.use("/api/", pingRouter);
 app.use("/api/result", resultRouter);
 app.use("/api/upload", uploadRouter);


app.use(errorHandler);
app.use(notFoundHandler);

/**
 * Server Activation
 */

 app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
  });

