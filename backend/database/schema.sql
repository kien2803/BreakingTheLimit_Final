-- BREAKING THE LIMITS DATABASE SCHEMA

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'student', -- 'student', 'parent', 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Journals table
CREATE TABLE journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    mood VARCHAR(50) NOT NULL, -- 'very-happy', 'happy', 'neutral', 'sad', 'very-sad', 'angry'
    emotion_positive FLOAT,
    emotion_neutral FLOAT,
    emotion_negative FLOAT,
    wellness_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Family connections table
CREATE TABLE family_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    relationship VARCHAR(50), -- 'father', 'mother', 'guardian'
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Privacy settings table
CREATE TABLE privacy_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    share_emotions BOOLEAN DEFAULT 1,
    alert_parents BOOLEAN DEFAULT 1,
    receive_messages BOOLEAN DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Daily messages table
CREATE TABLE daily_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    author VARCHAR(100) DEFAULT 'Breaking The Limits',
    display_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled', -- 'scheduled', 'published', 'archived'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Healing content table
CREATE TABLE healing_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'story', 'podcast', 'video'
    content TEXT NOT NULL,
    thumbnail_url VARCHAR(500),
    duration INTEGER, -- in seconds
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Drawings table
CREATE TABLE drawings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_data TEXT NOT NULL,
    prompt VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Saved messages table
CREATE TABLE saved_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES daily_messages(id) ON DELETE CASCADE
);

-- Alerts table
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    alert_type VARCHAR(50) NOT NULL, -- 'wellness_drop', 'negative_trend', 'crisis'
    severity VARCHAR(50) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Parent notifications table
CREATE TABLE parent_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    alert_id INTEGER,
    notification_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE
);

-- Letters to parents table
CREATE TABLE letters_to_parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'sent'
    moderation_note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Encouragement messages table
CREATE TABLE encouragement_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Activity log table
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_journals_user_date ON journals(user_id, created_at);
CREATE INDEX idx_journals_mood ON journals(mood);
CREATE INDEX idx_family_parent ON family_connections(parent_id);
CREATE INDEX idx_family_child ON family_connections(child_id);
CREATE INDEX idx_alerts_user ON alerts(user_id, is_resolved);
CREATE INDEX idx_notifications_parent ON parent_notifications(parent_id, is_read);
CREATE INDEX idx_activity_user ON activity_log(user_id, created_at);

-- Insert sample data
INSERT INTO users (name, email, password_hash, role) VALUES 
('Admin User', 'admin@btl.com', 'hashed_password', 'admin'),
('Nguyễn Văn A', 'student1@example.com', 'hashed_password', 'student'),
('Trần Thị B', 'parent1@example.com', 'hashed_password', 'parent');

INSERT INTO daily_messages (message, display_date, status) VALUES 
('Hít thật sâu, thở ra từ từ, bạn xứng đáng được bình yên.', DATE('now'), 'published'),
('Mỗi ngày là một khởi đầu mới, hãy tin vào bản thân.', DATE('now', '+1 day'), 'scheduled');

INSERT INTO healing_content (title, type, content, category) VALUES 
('Chiếc Lá Rụng Cuối Cùng', 'story', 'Full story content here...', 'Hy vọng'),
('Đứa Trẻ và Chiếc Cốc', 'story', 'Full story content here...', 'Tích cực'),
('Hạt Giống Của Niềm Tin', 'story', 'Full story content here...', 'Kiên nhẫn');