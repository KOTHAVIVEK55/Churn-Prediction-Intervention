const express = require('express');
const router = express.Router();
const whatsappController = require('../controllers/whatsappController');

// @route   POST /api/whatsapp/send
// @desc    Send a WhatsApp alert regarding student churn
// @access  Public (In production, this should be protected via middleware)
router.post('/send', whatsappController.sendChurnAlert);

module.exports = router;
