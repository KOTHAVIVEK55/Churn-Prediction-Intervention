const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret_for_development';

exports.register = async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    const normalizedEmail = email.toLowerCase().trim();
    
    let user = await User.findOne({ email: normalizedEmail });
    if (user) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    user = new User({
      email: normalizedEmail,
      password: hashedPassword
    });
    
    await user.save();

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
    
    const user = await User.findOne({ email: normalizedEmail });
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
