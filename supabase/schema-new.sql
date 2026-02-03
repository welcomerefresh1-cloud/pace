-- Users Table
CREATE TABLE users (
    user_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(11) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Degree Table
CREATE TABLE degrees (
    degree_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    degree_id VARCHAR(11) UNIQUE NOT NULL,
    degree_name VARCHAR(100) NOT NULL
);

-- Student Record Table
CREATE TABLE student_records (
    student_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id VARCHAR(10) UNIQUE NOT NULL,
    year_graduated INTEGER NOT NULL,
    gwa FLOAT NOT NULL,
    avg_prof_grade FLOAT,
    avg_elec_grade FLOAT,
    ojt_grade FLOAT,
    leadership_pos BOOLEAN,
    act_member_pos BOOLEAN,
    degree_code UUID NOT NULL REFERENCES degrees(degree_code) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Alumni Table
CREATE TABLE alumni (
    alumni_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alumni_id VARCHAR(11) UNIQUE NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    age INTEGER NOT NULL,
    user_code UUID REFERENCES users(user_code) ON DELETE SET NULL,
    student_code UUID NOT NULL REFERENCES student_records(student_code) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Skills Table
CREATE TABLE skills (
    skill_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id VARCHAR(11) UNIQUE NOT NULL,
    soft_skills_avg FLOAT,
    hard_skills_avg FLOAT,
    alumni_code UUID NOT NULL REFERENCES alumni(alumni_code) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Skills List Table
CREATE TABLE skills_list (
    sl_code UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_name VARCHAR(100) NOT NULL,
    skill_value FLOAT CHECK (skill_value >= 0 AND skill_value <= 100),
    skill_code UUID NOT NULL REFERENCES skills(skill_code) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_alumni_user_code ON alumni(user_code);
CREATE INDEX idx_alumni_student_code ON alumni(student_code);
CREATE INDEX idx_student_records_degree_code ON student_records(degree_code);
CREATE INDEX idx_skills_alumni_code ON skills(alumni_code);
CREATE INDEX idx_skills_list_skill_code ON skills_list(skill_code);
CREATE INDEX idx_student_records_year_graduated ON student_records(year_graduated);

-- Add comments for documentation
COMMENT ON TABLE users IS 'User authentication and account information';
COMMENT ON TABLE degrees IS 'Academic degree/course programs';
COMMENT ON TABLE student_records IS 'Academic records and performance data for graduated students';
COMMENT ON TABLE alumni IS 'Personal information of alumni linked to their academic records';
COMMENT ON TABLE skills IS 'Aggregate skill metrics (soft and hard skills averages) for each alumnus';
COMMENT ON TABLE skills_list IS 'Individual skill assessments and ratings for each alumnus';
