CREATE TABLE IF NOT EXISTS "pt_spec" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "spec_name" TEXT NOT NULL DEFAULT '',
  "remote_path" TEXT NOT NULL DEFAULT ''
);