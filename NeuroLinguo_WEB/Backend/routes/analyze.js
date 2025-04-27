const express = require('express');
const multer = require('multer');
const path = require('path');
const router = express.Router();
const fs = require('fs');
const verifyToken  = require('../middleware/verifyToken'); // Adjust the path as necessary
const {
  saveAnalyzeMessage,
  getAnalyzeMessagesBySession,
  getAllAnalyzeSessions
} = require('../controllers/analyzechatcontroller');

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      console.log(req.user);
      const userFolder = path.join(__dirname, `../database/${req.user.email}/uploads`);
      fs.mkdirSync(userFolder, { recursive: true });
      cb(null, userFolder);
    },
    filename: (req, file, cb) => {
      const timestamp = Date.now();
      const ext = path.extname(file.originalname);
      cb(null, `${path.basename(file.originalname, ext)}-${timestamp}${ext}`);
    }
  });
const upload = multer({ storage });
// For Saving Messages
router.post('/save', verifyToken, (req, res) => {
  const { sender, text, session_id,timestamp } = req.body;
  const email = req.user.email;

  if (!sender || !text || !session_id || !timestamp) {
    return res.status(400).json({ message: 'Missing fields' });
  }

  saveAnalyzeMessage(email, sender, text, session_id,timestamp);
  res.json({ message: 'Message saved' });
});
// For Getting All messages for a given Session
router.get('/history/:session_id', verifyToken, (req, res) => {
  const sessionId = req.params.session_id;
  const email = req.user.email;
  console.log(email,sessionId);
  getAnalyzeMessagesBySession(email, sessionId, (messages) => {
    res.json({ messages });
  });
});
// For Getting All Sessions for a given User
router.get('/sessions', verifyToken, (req, res) => {
  const email = req.user.email;

  getAllAnalyzeSessions(email, (sessions) => {
    res.json({ sessions });
  });
});


router.post('/upload',verifyToken, upload.single('pdf'), async (req, res) => {
  try {
    const file = req.file;
    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // TODO: PDF analysis logic goes here
    console.log('Received PDF:', file.originalname);

    res.json({ response: `Successfully analyzed: ${file.originalname}` });
  } catch (error) {
    console.error('Error analyzing PDF:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
