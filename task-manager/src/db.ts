import sqlite3 from 'sqlite3';
import { Database } from 'sqlite3';
import path from 'path';

const dbPath = path.resolve(__dirname, '../tasks.db');
export const db: Database = new sqlite3.Database(dbPath);
