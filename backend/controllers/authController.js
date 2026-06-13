const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');

const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret_for_development';
const USERS_FILE = path.join(__dirname, '..', 'users.json');

// Helper to read users from the local file fallback
function getLocalUsers() {
  if (!fs.existsSync(USERS_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(USERS_FILE, 'utf8'));
  } catch (err) {
    console.error('Error reading local users file:', err.message);
    return [];
  }
}

// Helper to save users to the local file fallback
function saveLocalUsers(users) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), 'utf8');
  } catch (err) {
    console.error('Error writing local users file:', err.message);
  }
}

exports.register = async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    const normalizedEmail = email.toLowerCase().trim();
    let user;
    const isMongoConnected = mongoose.connection.readyState === 1;

    if (isMongoConnected) {
      user = await User.findOne({ email: normalizedEmail });
    } else {
      console.warn('[WARNING] MongoDB is not connected. Using local JSON database file fallback.');
      const localUsers = getLocalUsers();
      user = localUsers.find(u => u.email === normalizedEmail);
    }

    if (user) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    let userId;
    if (isMongoConnected) {
      user = new User({
        email: normalizedEmail,
        password: hashedPassword
      });
      await user.save();
      userId = user.id;
    } else {
      userId = 'local_' + Date.now();
      user = {
        id: userId,
        email: normalizedEmail,
        password: hashedPassword,
        role: 'user',
        createdAt: new Date()
      };
      const localUsers = getLocalUsers();
      localUsers.push(user);
      saveLocalUsers(localUsers);
    }

    // Create token
    const payload = {
      user: {
        id: userId
      }
    };

    jwt.sign(
      payload,
      JWT_SECRET,
      { expiresIn: '5h' },
      (err, token) => {
        if (err) throw err;
        res.status(201).json({ token, message: 'User registered successfully' });
      }
    );
  } catch (err) {
    console.error('Error in register:', err.message);
    res.status(500).json({ message: 'Server Error: ' + err.message });
  }
};

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    const normalizedEmail = email.toLowerCase().trim();
    let user;
    const isMongoConnected = mongoose.connection.readyState === 1;

    if (isMongoConnected) {
      user = await User.findOne({ email: normalizedEmail });
    } else {
      console.warn('[WARNING] MongoDB is not connected. Using local JSON database file fallback.');
      const localUsers = getLocalUsers();
      user = localUsers.find(u => u.email === normalizedEmail);
    }

    if (!user) {
      return res.status(400).json({ message: 'Invalid Credentials' });
    }

    // Compare passwords
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid Credentials' });
    }

    // Create token
    const payload = {
      user: {
        id: user.id || user._id
      }
    };

    jwt.sign(
      payload,
      JWT_SECRET,
      { expiresIn: '5h' },
      (err, token) => {
        if (err) throw err;
        res.status(200).json({ token, message: 'Login successful' });
      }
    );
  } catch (err) {
    console.error('Error in login:', err.message);
    res.status(500).json({ message: 'Server Error: ' + err.message });
  }
};
