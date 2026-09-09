SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- Mevcut bir Macera Akademi veritabanına öğretmen paneli oturumlarını ekler.
-- Yeni kurulumlarda aynı tablo schema.sql tarafından oluşturulur.
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
