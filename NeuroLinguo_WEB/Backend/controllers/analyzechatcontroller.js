const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

function getAnalyzeDBPath(email) {
  const userDir = path.join(__dirname, `../database/${email}`);
  fs.mkdirSync(userDir, { recursive: true });
  return path.join(userDir, 'analyzechats.db');
}
function initializeAnalyzeDB(dbPath) {
  const db = new sqlite3.Database(dbPath);
  db.run(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sender TEXT,
      text TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      session_id TEXT
    )
  `);
  return db;
}
function saveAnalyzeMessage(email, sender, text, sessionId,timestamp) {
  const dbPath = getAnalyzeDBPath(email);
  const db = initializeAnalyzeDB(dbPath);

  const stmt = db.prepare(`
    INSERT INTO messages (sender, text, session_id,timestamp)
    VALUES (?, ?, ?, ?)
  `);
  stmt.run(sender, text, sessionId, function (err) {
    if (err) console.error('Error saving analyze message:', err);
  });
  stmt.finalize();
  db.close();
}
function getAnalyzeMessagesBySession(email, sessionId, callback) {
  const dbPath = getAnalyzeDBPath(email);
  const db = initializeAnalyzeDB(dbPath);
  // WHERE session_id = ?

  db.all(`
    SELECT * FROM messages
    ORDER BY timestamp ASC

  `, (err, rows) => {
    if (err) {
      console.error('Error fetching analyze messages:', err);
      callback([]);
    } else {
      callback(rows);
    }
    db.close();
  });
}
function getAllAnalyzeSessions(email, callback) {
  const dbPath = getAnalyzeDBPath(email);
  const db = initializeAnalyzeDB(dbPath);

  console.log('Fetching all sessions for user:', email);
  db.all(`
    FROM messages
    SELECT DISTINCT session_id
    ORDER BY MAX(timestamp) DESC
  `, [], (err, rows) => {
    if (err) {
      console.error('Error fetching sessions:', err);
      callback([]);
    } else {
      const sessions = rows.map(row => row.session_id);
      callback(sessions);
    }
    db.close();
  });
}


module.exports = {
  getAnalyzeDBPath,
  initializeAnalyzeDB,
  saveAnalyzeMessage,
  getAnalyzeMessagesBySession,
  getAllAnalyzeSessions
};
