CREATE TABLE IF NOT EXISTS "pt_code_repo" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL DEFAULT '',
  "remote_path" TEXT NOT NULL DEFAULT '',
  "username" TEXT NOT NULL DEFAULT '',
  "password" TEXT NOT NULL DEFAULT '',
  "type" INTEGER NOT NULL DEFAULT 0  /* 1=>svn, 2=>git */
);