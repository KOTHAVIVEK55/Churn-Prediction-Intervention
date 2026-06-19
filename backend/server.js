require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve Static Frontend UI
app.use(express.static(path.join(__dirname, 'public')));

// Routes

const mlWarningHTML = `
  <div style="font-family: sans-serif; padding: 40px; text-align: center; color: white; background: #0b1020; height: 100vh;">
    <h1>⚠️ Machine Learning Model Offline</h1>
    <p>This ML model requires a persistent Python server (Gradio) and cannot run on Vercel's Serverless architecture.</p>
    <p>Please deploy the <b>ai_school</b> folder to <a href="https://huggingface.co/spaces" style="color: #6366f1;">Hugging Face Spaces</a> or Render.com, and update your frontend buttons to link there!</p>
  </div>
`;

app.get('/churn', (req, res) => res.status(503).send(mlWarningHTML));
app.get('/growth', (req, res) => res.status(503).send(mlWarningHTML));
app.get('/future', (req, res) => res.status(503).send(mlWarningHTML));

app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/whatsapp', require('./routes/whatsappRoutes'));

// Fallback for SPA (if needed in future)
// We rely on express.static serving index.html for the root route.

// Connect to MongoDB
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/school_analytics';

mongoose.connect(MONGO_URI)
  .then(() => {
    console.log('MongoDB connected successfully');
  })
  .catch((err) => {
    console.error('MongoDB connection error:', err.message);
    console.warn('Backend server will continue running using local JSON database fallback.');
  });

if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => {
    console.log(`Node.js Backend server running on port ${PORT}`);
  });
}

module.exports = app;
