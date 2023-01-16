
-- single line comment
/* Comment block */

--DROP DATABASE DevOps_TeamTwo_2022;

CREATE DATABASE DevOps_TeamTwo_2022;


--=====================================================
--=====================================================
--=====================================================
--DROP TABLE Internship_Student_Data;

CREATE TABLE Internship_Student_Data (
    StudentID varchar(10) NOT NULL PRIMARY KEY CLUSTERED,
    Name varchar(255) NOT NULL,
    Preference varchar(255) NOT NULL,
    Status varchar(11) NOT NULL
);

--DELETE FROM Internship_Student_Data WHERE StudentID='S12345670A';

INSERT INTO Internship_Student_Data VALUES ('S12345670A', 'Student 1','Software Development','Unassigned');

--=====================================================
--=====================================================
--=====================================================

--DROP TABLE Internship_Company_Data;

CREATE TABLE Internship_Company_Data (
	ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,
    Company_Name varchar(255) NOT NULL,
    Job_Role varchar(255) NOT NULL,
    Company_Contact varchar(255) NOT NULL,
    Email varchar(255) NOT NULL
);

--DELETE FROM Internship_Company_Data WHERE Company_Name='Company A';

INSERT INTO Internship_Company_Data (Company_Name, Job_Role, Company_Contact, Email) VALUES ('Company A', 'Software Developer','Mr A','devopsTeam2Company1');

--=====================================================
--=====================================================
--=====================================================

--DROP TABLE Internship_Information_Data;

CREATE TABLE Internship_Information_Data (
	StudentID varchar(10) not null primary key foreign key references Internship_Student_Data(StudentID),
	ID INT not null foreign key references Internship_Company_Data(ID)
);

--DELETE FROM Internship_Information_Data WHERE StudentID='S12345670A';

INSERT INTO Internship_Information_Data VALUES ('S12345670A', 1);

--=====================================================
--=====================================================
--=====================================================

SELECT * FROM Internship_Information_Data;