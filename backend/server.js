import express from 'express';
import authRoutes from "./routes/auth.route.js";
import movieRoutes from "./routes/movie.route.js"
import tvRoutes from "./routes/tv.route.js"
import searchRoutes from "./routes/search.route.js";
import cookieParser from "cookie-parser";
import { protectRoute } from './middleware/protectRoute.js';
import { ENV_VARS } from './config/envVars.js';
import { connectDB } from './config/db.js';
import cors from 'cors';

// Enable CORS for all routes


const app = express();
const port = ENV_VARS.PORT;

app.use(cors());
app.use(express.json());
app.use(cookieParser());

app.use("/api/v1/auth",  authRoutes);
app.use("/api/v1/movie", movieRoutes);
app.use("/api/v1/tv", tvRoutes);
app.use("/api/v1/search", searchRoutes);

app.listen(port, () => {
    console.log("Testing at 5000 ");
    connectDB(); 
});