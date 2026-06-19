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

// Provide external ML App links to the frontend
app.get('/api/config', (req, res) => {
    const hfSpaceUrl = "https://huggingface.co/spaces/Vivek1000/school-ai-model";
    res.json({
        churnUrl: hfSpaceUrl,
        growthUrl: hfSpaceUrl,
        futureUrl: hfSpaceUrl
    });
});

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
