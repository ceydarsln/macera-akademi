SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- Mevcut veritabanında eski asenkron duels tablolarını değiştirmeden uygula.
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
