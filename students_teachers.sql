-- Create the 'students' table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    email VARCHAR(100)
);

-- Create the 'teachers' table
CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    subject VARCHAR(100),
    email VARCHAR(100)
);
