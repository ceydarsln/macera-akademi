SET NAMES utf8mb4;
SET time_zone = '+00:00';

CREATE TABLE IF NOT EXISTS teachers (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(120) NOT NULL DEFAULT '',
  email VARCHAR(190) NOT NULL DEFAULT '',
  active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_teachers_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS classes (
  code VARCHAR(32) NOT NULL,
  teacher_id BIGINT UNSIGNED NULL,
  teacher_name VARCHAR(120) NOT NULL DEFAULT '',
  name VARCHAR(120) NOT NULL DEFAULT '',
  grade TINYINT UNSIGNED NOT NULL DEFAULT 1,
  active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (code),
  KEY idx_classes_teacher (teacher_id),
  CONSTRAINT fk_classes_teacher FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS teacher_tokens (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  teacher_id BIGINT UNSIGNED NOT NULL,
  token_hash BINARY(32) NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_used_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_teacher_tokens_hash (token_hash),
  KEY idx_teacher_tokens_teacher (teacher_id),
  KEY idx_teacher_tokens_expiry (expires_at),
  CONSTRAINT fk_teacher_tokens_teacher FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(60) NOT NULL,
  username_key VARCHAR(60) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  parent_email VARCHAR(190) NOT NULL DEFAULT '',
  password_hash VARCHAR(255) NOT NULL,
  grade TINYINT UNSIGNED NOT NULL DEFAULT 1,
  level INT UNSIGNED NOT NULL DEFAULT 1,
  xp INT UNSIGNED NOT NULL DEFAULT 0,
  coins INT UNSIGNED NOT NULL DEFAULT 0,
  coins_earned INT UNSIGNED NOT NULL DEFAULT 0,
  look_json LONGTEXT NOT NULL,
  owned_json LONGTEXT NOT NULL,
  badges_json LONGTEXT NOT NULL,
  duel_stats_json LONGTEXT NOT NULL,
  settings_json LONGTEXT NOT NULL,
  completed_json LONGTEXT NOT NULL,
  teacher_code VARCHAR(32) NULL,
  teacher_name VARCHAR(120) NOT NULL DEFAULT '',
  teacher_id BIGINT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  last_login_at DATETIME NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username_key (username_key),
  KEY idx_users_teacher_code (teacher_code),
  KEY idx_users_teacher_id (teacher_id),
  CONSTRAINT fk_users_class FOREIGN KEY (teacher_code) REFERENCES classes (code) ON DELETE SET NULL,
  CONSTRAINT fk_users_teacher FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS api_tokens (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  token_hash BINARY(32) NOT NULL,
  expires_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_used_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_api_tokens_hash (token_hash),
  KEY idx_api_tokens_user (user_id),
  KEY idx_api_tokens_expiry (expires_at),
  CONSTRAINT fk_api_tokens_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS api_rate_limits (
  rate_key CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  attempts INT UNSIGNED NOT NULL DEFAULT 0,
  window_started_at DATETIME NOT NULL,
  PRIMARY KEY (rate_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS friendships (
  user_low_id BIGINT UNSIGNED NOT NULL,
  user_high_id BIGINT UNSIGNED NOT NULL,
  requester_id BIGINT UNSIGNED NOT NULL,
  status ENUM('pending','accepted','blocked') NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_low_id, user_high_id),
  KEY idx_friendships_high (user_high_id),
  KEY idx_friendships_requester (requester_id),
  CONSTRAINT fk_friendships_low FOREIGN KEY (user_low_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_friendships_high FOREIGN KEY (user_high_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_friendships_requester FOREIGN KEY (requester_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS messages (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  from_user_id BIGINT UNSIGNED NOT NULL,
  to_user_id BIGINT UNSIGNED NOT NULL,
  preset_id ENUM('selam','iyi_oyun','tebrikler','yarisalim','harikaydin','gorusuruz') NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  read_at DATETIME NULL,
  PRIMARY KEY (id),
  KEY idx_messages_to (to_user_id, created_at),
  KEY idx_messages_from (from_user_id),
  CONSTRAINT fk_messages_from FOREIGN KEY (from_user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_messages_to FOREIGN KEY (to_user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS duels (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  from_user_id BIGINT UNSIGNED NOT NULL,
  to_user_id BIGINT UNSIGNED NOT NULL,
  from_name VARCHAR(60) NOT NULL,
  to_name VARCHAR(60) NOT NULL,
  grade TINYINT UNSIGNED NOT NULL,
  category_id VARCHAR(40) NOT NULL,
  category_label VARCHAR(100) NOT NULL,
  seed BIGINT NOT NULL,
  status ENUM('pending','done') NOT NULL DEFAULT 'pending',
  from_score INT NOT NULL DEFAULT 0,
  from_correct INT NOT NULL DEFAULT 0,
  from_answers_json LONGTEXT NOT NULL,
  to_score INT NULL,
  to_correct INT NULL,
  to_answers_json LONGTEXT NULL,
  winner_user_id BIGINT UNSIGNED NULL,
  is_draw TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  played_at DATETIME NULL,
  PRIMARY KEY (id),
  KEY idx_duels_from (from_user_id, created_at),
  KEY idx_duels_to (to_user_id, created_at),
  CONSTRAINT fk_duels_from FOREIGN KEY (from_user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_duels_to FOREIGN KEY (to_user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_duels_winner FOREIGN KEY (winner_user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS duel_claims (
  duel_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  claimed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (duel_id, user_id),
  CONSTRAINT fk_duel_claims_duel FOREIGN KEY (duel_id) REFERENCES duels (id) ON DELETE CASCADE,
  CONSTRAINT fk_duel_claims_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Canlı maçlar eski, sonradan oynanan duels kayıtlarından bağımsızdır.
CREATE TABLE IF NOT EXISTS live_matches (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  from_user_id BIGINT UNSIGNED NOT NULL,
  to_user_id BIGINT UNSIGNED NOT NULL,
  from_name VARCHAR(60) NOT NULL,
  to_name VARCHAR(60) NOT NULL,
  grade TINYINT UNSIGNED NOT NULL,
  category_id VARCHAR(40) NOT NULL,
  category_label VARCHAR(100) NOT NULL,
  questions_json LONGTEXT NOT NULL,
  status ENUM('invited','lobby','countdown','playing','finished','declined','cancelled','expired') NOT NULL DEFAULT 'invited',
  from_ready TINYINT(1) NOT NULL DEFAULT 0,
  to_ready TINYINT(1) NOT NULL DEFAULT 0,
  from_score INT UNSIGNED NOT NULL DEFAULT 0,
  to_score INT UNSIGNED NOT NULL DEFAULT 0,
  from_correct TINYINT UNSIGNED NOT NULL DEFAULT 0,
  to_correct TINYINT UNSIGNED NOT NULL DEFAULT 0,
  winner_user_id BIGINT UNSIGNED NULL,
  forfeit_user_id BIGINT UNSIGNED NULL,
  finish_reason ENUM('score','forfeit') NOT NULL DEFAULT 'score',
  is_draw TINYINT(1) NOT NULL DEFAULT 0,
  invite_expires_at DATETIME(3) NOT NULL,
  lobby_expires_at DATETIME(3) NULL,
  starts_at DATETIME(3) NULL,
  ends_at DATETIME(3) NULL,
  from_last_seen_at DATETIME(3) NULL,
  to_last_seen_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (id),
  KEY idx_live_matches_from (from_user_id, status, created_at),
  KEY idx_live_matches_to (to_user_id, status, created_at),
  CONSTRAINT fk_live_matches_from FOREIGN KEY (from_user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_live_matches_to FOREIGN KEY (to_user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_live_matches_winner FOREIGN KEY (winner_user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS live_match_answers (
  match_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  question_index TINYINT UNSIGNED NOT NULL,
  option_index TINYINT UNSIGNED NOT NULL,
  is_correct TINYINT(1) NOT NULL,
  response_ms INT UNSIGNED NOT NULL,
  points TINYINT UNSIGNED NOT NULL,
  answered_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (match_id, user_id, question_index),
  KEY idx_live_match_answers_user (user_id, match_id),
  CONSTRAINT fk_live_answers_match FOREIGN KEY (match_id) REFERENCES live_matches (id) ON DELETE CASCADE,
  CONSTRAINT fk_live_answers_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS live_match_claims (
  match_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  reward_json LONGTEXT NOT NULL,
  claimed_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (match_id, user_id),
  KEY idx_live_match_claims_user (user_id, claimed_at),
  CONSTRAINT fk_live_claims_match FOREIGN KEY (match_id) REFERENCES live_matches (id) ON DELETE CASCADE,
  CONSTRAINT fk_live_claims_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS assignments (
  id VARCHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  class_code VARCHAR(32) NOT NULL,
  title VARCHAR(160) NOT NULL,
  grade TINYINT UNSIGNED NULL,
  subject VARCHAR(40) NOT NULL DEFAULT '',
  game_ids_json LONGTEXT NOT NULL,
  due_date DATE NULL,
  note VARCHAR(500) NOT NULL DEFAULT '',
  active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_assignments_class (class_code, active, created_at),
  CONSTRAINT fk_assignments_class FOREIGN KEY (class_code) REFERENCES classes (code) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contests (
  id VARCHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  class_code VARCHAR(32) NOT NULL,
  title VARCHAR(160) NOT NULL,
  kind ENUM('daily','weekly') NOT NULL DEFAULT 'daily',
  category_id VARCHAR(40) NOT NULL DEFAULT 'mix',
  category_label VARCHAR(100) NOT NULL DEFAULT '',
  grade TINYINT UNSIGNED NOT NULL DEFAULT 1,
  seed BIGINT NOT NULL DEFAULT 1,
  starts_at DATE NULL,
  ends_at DATE NULL,
  active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_contests_class (class_code, active, starts_at, ends_at),
  CONSTRAINT fk_contests_class FOREIGN KEY (class_code) REFERENCES classes (code) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS class_progress (
  class_code VARCHAR(32) NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  username VARCHAR(60) NOT NULL,
  grade TINYINT UNSIGNED NOT NULL,
  level INT UNSIGNED NOT NULL DEFAULT 1,
  xp INT UNSIGNED NOT NULL DEFAULT 0,
  coins INT UNSIGNED NOT NULL DEFAULT 0,
  done_count INT UNSIGNED NOT NULL DEFAULT 0,
  done_ids_json LONGTEXT NOT NULL,
  duel_wins INT UNSIGNED NOT NULL DEFAULT 0,
  duel_best INT UNSIGNED NOT NULL DEFAULT 0,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (class_code, user_id),
  KEY idx_class_progress_user (user_id),
  CONSTRAINT fk_class_progress_class FOREIGN KEY (class_code) REFERENCES classes (code) ON DELETE CASCADE,
  CONSTRAINT fk_class_progress_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contest_scores (
  contest_id VARCHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  class_code VARCHAR(32) NOT NULL,
  username VARCHAR(60) NOT NULL,
  score INT UNSIGNED NOT NULL DEFAULT 0,
  correct_count INT UNSIGNED NOT NULL DEFAULT 0,
  grade TINYINT UNSIGNED NOT NULL,
  submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (contest_id, user_id),
  KEY idx_contest_scores_class (class_code),
  KEY idx_contest_scores_rank (contest_id, score),
  CONSTRAINT fk_contest_scores_contest FOREIGN KEY (contest_id) REFERENCES contests (id) ON DELETE CASCADE,
  CONSTRAINT fk_contest_scores_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT fk_contest_scores_class FOREIGN KEY (class_code) REFERENCES classes (code) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
