BEGIN;
--
-- Create model AcademicSession
--
CREATE TABLE "school_app_academicsession" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(20) NOT NULL UNIQUE, "start_date" date NOT NULL, "end_date" date NOT NULL);
--
-- Create model Calendar
--
CREATE TABLE "school_app_calendar" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "event_name" varchar(255) NOT NULL, "description" text NOT NULL, "event_date" date NULL, "start_time" time NULL, "end_time" time NULL, "event_type" varchar NOT NULL);
--
-- Create model Post
--
CREATE TABLE "school_app_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(5000) NOT NULL, "content" varchar(5000) NOT NULL, "is_image" varchar(100) NULL, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "school_app_post_likes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "post_id" bigint NOT NULL REFERENCES "school_app_post" ("id") DEFERRABLE INITIALLY DEFERRED, "customuser_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Announcement
--
CREATE TABLE "school_app_announcement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(50) NOT NULL, "information" varchar(10000) NOT NULL, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Department
--
CREATE TABLE "school_app_department" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(100) NOT NULL UNIQUE, "dept_code" varchar(10) NOT NULL UNIQUE, "faculty" varchar(100) NOT NULL, "hod_id" bigint NULL UNIQUE REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Course
--
CREATE TABLE "school_app_course" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "course_name" varchar(100) NOT NULL, "code" varchar(10) NOT NULL UNIQUE, "description" text NULL, "credit_units" smallint unsigned NOT NULL CHECK ("credit_units" >= 0), "level" smallint unsigned NOT NULL CHECK ("level" >= 0), "semester" varchar(20) NOT NULL, "department_id" bigint NOT NULL REFERENCES "school_app_department" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "school_app_course_lecturer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "course_id" bigint NOT NULL REFERENCES "school_app_course" ("id") DEFERRABLE INITIALLY DEFERRED, "customuser_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Exam
--
CREATE TABLE "school_app_exam" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "date" date NOT NULL, "duration" bigint NOT NULL, "total_marks" integer unsigned NOT NULL CHECK ("total_marks" >= 0), "semester" varchar(100) NOT NULL, "exam_type" varchar(20) NOT NULL, "academic_session_id" bigint NULL REFERENCES "school_app_academicsession" ("id") DEFERRABLE INITIALLY DEFERRED, "course_id" bigint NOT NULL REFERENCES "school_app_course" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NOT NULL REFERENCES "school_app_department" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IdentityCard
--
CREATE TABLE "school_app_identitycard" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "picture" varchar(100) NOT NULL, "faculty" varchar(50) NOT NULL, "admission_number_id" bigint NULL REFERENCES "accounts_app_student" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NULL REFERENCES "school_app_department" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL UNIQUE REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Lecture
--
CREATE TABLE "school_app_lecture" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "start_time" datetime NOT NULL, "duration" bigint NOT NULL, "venue" varchar(150) NOT NULL, "course_id" bigint NOT NULL REFERENCES "school_app_course" ("id") DEFERRABLE INITIALLY DEFERRED, "lecturer_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Notification
--
CREATE TABLE "school_app_notification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "message" text NOT NULL, "is_read" bool NOT NULL, "link" varchar(500) NULL, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Payment
--
CREATE TABLE "school_app_payment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "admin_fee" decimal NOT NULL, "course_fee" decimal NOT NULL, "library_fee" decimal NOT NULL, "total" decimal NULL, "status" varchar NULL, "transaction_id" varchar(20) NULL, "admission_number_id" bigint NOT NULL REFERENCES "accounts_app_student" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Comment
--
CREATE TABLE "school_app_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "description" text NOT NULL, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "post_id" bigint NOT NULL REFERENCES "school_app_post" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Question
--
CREATE TABLE "school_app_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "text" text NOT NULL, "is_image" varchar(100) NULL, "option_a" varchar(255) NOT NULL, "option_b" varchar(255) NOT NULL, "option_c" varchar(255) NOT NULL, "option_d" varchar(255) NOT NULL, "correct_option" varchar(1) NOT NULL, "mark" integer unsigned NOT NULL CHECK ("mark" >= 0), "exam_id" bigint NOT NULL REFERENCES "school_app_exam" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Receipt
--
CREATE TABLE "school_app_receipt" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "receipt_number" varchar(30) NULL UNIQUE, "issue_date" datetime NOT NULL, "admin_fee" decimal NOT NULL, "course_fee" decimal NOT NULL, "library_fee" decimal NOT NULL, "total_amount" decimal NOT NULL, "payment_status" varchar(20) NOT NULL, "payment_id" bigint NOT NULL UNIQUE REFERENCES "school_app_payment" ("id") DEFERRABLE INITIALLY DEFERRED, "student_name_id" bigint NULL REFERENCES "accounts_app_student" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Result
--
CREATE TABLE "school_app_result" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "score" decimal NULL, "grade" varchar(2) NULL, "admission_number_id" bigint NULL REFERENCES "accounts_app_student" ("id") DEFERRABLE INITIALLY DEFERRED, "course_id" bigint NULL REFERENCES "school_app_course" ("id") DEFERRABLE INITIALLY DEFERRED, "exam_id" bigint NULL REFERENCES "school_app_exam" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model TimeTable
--
CREATE TABLE "school_app_timetable" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "week_day" varchar NOT NULL, "start_time" time NULL, "end_time" time NULL, "semester" varchar(20) NULL, "duration" bigint NOT NULL, "venue" varchar(150) NOT NULL, "academic_session_id" bigint NULL REFERENCES "school_app_academicsession" ("id") DEFERRABLE INITIALLY DEFERRED, "course_id" bigint NULL REFERENCES "school_app_course" ("id") DEFERRABLE INITIALLY DEFERRED, "lecturer_id" bigint NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Repost
--
CREATE TABLE "school_app_repost" ("post_ptr_id" bigint NOT NULL PRIMARY KEY REFERENCES "school_app_post" ("id") DEFERRABLE INITIALLY DEFERRED, "original_post_id" bigint NOT NULL REFERENCES "school_app_post" ("id") DEFERRABLE INITIALLY DEFERRED, "reposted_by_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "school_app_post_user_id_33929071" ON "school_app_post" ("user_id");
CREATE UNIQUE INDEX "school_app_post_likes_post_id_customuser_id_f86647c1_uniq" ON "school_app_post_likes" ("post_id", "customuser_id");
CREATE INDEX "school_app_post_likes_post_id_31195f3f" ON "school_app_post_likes" ("post_id");
CREATE INDEX "school_app_post_likes_customuser_id_309efbbb" ON "school_app_post_likes" ("customuser_id");
CREATE INDEX "school_app_announcement_user_id_7f0bc42c" ON "school_app_announcement" ("user_id");
CREATE INDEX "school_app_course_department_id_0da0c964" ON "school_app_course" ("department_id");
CREATE UNIQUE INDEX "school_app_course_lecturer_course_id_customuser_id_c70a1f18_uniq" ON "school_app_course_lecturer" ("course_id", "customuser_id");
CREATE INDEX "school_app_course_lecturer_course_id_4ad14922" ON "school_app_course_lecturer" ("course_id");
CREATE INDEX "school_app_course_lecturer_customuser_id_aa13c8cd" ON "school_app_course_lecturer" ("customuser_id");
CREATE INDEX "school_app_exam_academic_session_id_cd8eb39f" ON "school_app_exam" ("academic_session_id");
CREATE INDEX "school_app_exam_course_id_b5c33c57" ON "school_app_exam" ("course_id");
CREATE INDEX "school_app_exam_department_id_ac9c09ba" ON "school_app_exam" ("department_id");
CREATE INDEX "school_app_identitycard_admission_number_id_44112ffb" ON "school_app_identitycard" ("admission_number_id");
CREATE INDEX "school_app_identitycard_department_id_25f6f5e0" ON "school_app_identitycard" ("department_id");
CREATE INDEX "school_app_lecture_course_id_982d3c36" ON "school_app_lecture" ("course_id");
CREATE INDEX "school_app_lecture_lecturer_id_28443585" ON "school_app_lecture" ("lecturer_id");
CREATE INDEX "school_app_notification_user_id_fdfacc04" ON "school_app_notification" ("user_id");
CREATE INDEX "school_app_payment_admission_number_id_b99b995c" ON "school_app_payment" ("admission_number_id");
CREATE INDEX "school_app_payment_user_id_eeef2404" ON "school_app_payment" ("user_id");
CREATE INDEX "school_app_comment_user_id_96f0c4dd" ON "school_app_comment" ("user_id");
CREATE INDEX "school_app_comment_post_id_1cc4f3f1" ON "school_app_comment" ("post_id");
CREATE INDEX "school_app_question_exam_id_9ead48c1" ON "school_app_question" ("exam_id");
CREATE INDEX "school_app_receipt_student_name_id_5548e5c0" ON "school_app_receipt" ("student_name_id");
CREATE INDEX "school_app_result_admission_number_id_64962ee9" ON "school_app_result" ("admission_number_id");
CREATE INDEX "school_app_result_course_id_b0e5df58" ON "school_app_result" ("course_id");
CREATE INDEX "school_app_result_exam_id_a0c838b9" ON "school_app_result" ("exam_id");
CREATE INDEX "school_app_result_user_id_079e8fc9" ON "school_app_result" ("user_id");
CREATE INDEX "school_app_timetable_academic_session_id_e0227b53" ON "school_app_timetable" ("academic_session_id");
CREATE INDEX "school_app_timetable_course_id_ebb1df77" ON "school_app_timetable" ("course_id");
CREATE INDEX "school_app_timetable_lecturer_id_228ab988" ON "school_app_timetable" ("lecturer_id");
CREATE INDEX "school_app_repost_original_post_id_800bcf8c" ON "school_app_repost" ("original_post_id");
CREATE INDEX "school_app_repost_reposted_by_id_a6391e27" ON "school_app_repost" ("reposted_by_id");
COMMIT;
