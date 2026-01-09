import { db } from './db.js';

const up = () => {
  db.serialize(() => {
    db.run(`
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT CHECK(priority IN ('high', 'medium', 'low')) NOT NULL DEFAULT 'medium',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `, (err) => {
      if (err) {
        console.error('Migration failed:', err);
        process.exit(1);
      } else {
        console.log('Migration successful: tasks table created with priority column.');
        process.exit(0);
      }
    });
  });
};

up();
