BEGIN;
--
-- Create model AcademicSession
--
CREATE TABLE "accounts_app_academicsession" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(20) NOT NULL UNIQUE, "start_date" date NOT NULL, "end_date" date NOT NULL);
--
-- Create model AdmissionNumberCounter
--
CREATE TABLE "accounts_app_admissionnumbercounter" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "year" integer NOT NULL UNIQUE, "last_number" integer NOT NULL);
--
-- Create model Student
--
CREATE TABLE "accounts_app_student" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "date_of_birth" date NULL, "admission_number" varchar(50) NULL UNIQUE, "faculty" varchar(50) NOT NULL, "picture" varchar(100) NULL, "level" smallint unsigned NOT NULL CHECK ("level" >= 0));
--
-- Create model CustomUser
--
CREATE TABLE "accounts_app_customuser" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "username" varchar(100) NOT NULL UNIQUE, "email" varchar(100) NOT NULL UNIQUE, "phone_number" varchar(20) NULL, "user_type" varchar(20) NULL, "date_joined" datetime NOT NULL, "is_admin" bool NOT NULL, "is_hod" bool NOT NULL, "is_active" bool NOT NULL, "is_staff" bool NOT NULL, "is_superuser" bool NOT NULL);
CREATE TABLE "accounts_app_customuser_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "accounts_app_customuser_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "customuser_id" bigint NOT NULL REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model LecturerProfile
--
CREATE TABLE "accounts_app_lecturerprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "staff_id" varchar(100) NULL, "rank" varchar(100) NULL, "office_location" varchar(100) NULL, "picture" varchar(100) NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "accounts_app_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "accounts_app_customuser_groups_customuser_id_group_id_0dd23bdc_uniq" ON "accounts_app_customuser_groups" ("customuser_id", "group_id");
CREATE INDEX "accounts_app_customuser_groups_customuser_id_df5422f8" ON "accounts_app_customuser_groups" ("customuser_id");
CREATE INDEX "accounts_app_customuser_groups_group_id_f9f8ca73" ON "accounts_app_customuser_groups" ("group_id");
CREATE UNIQUE INDEX "accounts_app_customuser_user_permissions_customuser_id_permission_id_b8ef9832_uniq" ON "accounts_app_customuser_user_permissions" ("customuser_id", "permission_id");
CREATE INDEX "accounts_app_customuser_user_permissions_customuser_id_5b9b34ef" ON "accounts_app_customuser_user_permissions" ("customuser_id");
CREATE INDEX "accounts_app_customuser_user_permissions_permission_id_8d347ed9" ON "accounts_app_customuser_user_permissions" ("permission_id");
COMMIT;
