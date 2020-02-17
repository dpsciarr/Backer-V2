# Backer-V2
V2 for Backer Application

### Updates from V1:
- Database migration from MySQL to SQLite
- More structured codebase than V1
   - Easier to scale and add functionality

## Description of Backup Procedures:

### File Copy New:

Select a source folder and a destination folder. The files in the source folder are copied to the destination folder. This is not recursive, meaning the files within the child source folders are not copied, only the files directly in the source folder are copied.

If the file already exists the file is still copied, but with a suffix determined by the "Suffix" setting:
1. Basic:
   - Appends a numeric to the end of the newly copied file(s).
2. Date:
   - Appends the date to the end of the newly copied file(s).
3. Date-Time:
   - Appends the date and time to the end of the newly copied file(s).
4. Timestamp:
   - Appends a timestamp to the end of the newly copied file(s).

### Single File Copy New:

Select a source file and a destination folder. The selected source file will be copied into the destination folder.
