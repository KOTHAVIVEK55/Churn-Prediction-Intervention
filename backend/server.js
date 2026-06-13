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
const { createProxyMiddleware } = require('http-proxy-middleware');

// Proxy routes to Python Gradio apps
app.use('/churn', createProxyMiddleware({ target: 'http://127.0.0.1:7860', changeOrigin: true, ws: true }));
app.use('/growth', createProxyMiddleware({ target: 'http://127.0.0.1:1000', changeOrigin: true, ws: true }));
app.use('/future', createProxyMiddleware({ target: 'http://127.0.0.1:1002', changeOrigin: true, ws: true }));

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

app.listen(PORT, () => {
  console.log(`Node.js Backend server running on port ${PORT}`);
});
