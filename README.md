# Backer-V2
Backup Management Configuration Software

### Updates from V1:
- Database migration from MySQL to SQLite
- More structured codebase than V1
   - Easier to scale and add functionality

## Description of Backup Procedures:

### File Copy New:

Select a source folder and a destination folder. The files in the source folder are copied to the destination folder. This is not recursive, meaning the files within the child source folders are not copied, only the files directly in the source folder are copied.

If the file already exists then the file is still copied, but with a suffix determined by the "Suffix" setting. See appendix A.

### Single File Copy New:

Select a source file and a destination folder. The selected source file will be copied into the destination folder. If the filename exists in the destination folder then the file is still copied, but with an appended suffix detailed in Appendix A.

### File Copy Overwrite:

Select a source folder and a destination folder. The files in the source folder are copied to the destination folder. This is not recursive, meaning the files within the child source folders are not copied, only the files directly in the source folder are copied.

If the file already exists in the destination folder then the file overwrites the existing file.

### Single File Copy Overwrite:

Select a source file and a destination folder. The selected source file will be copied into the destination folder. If the filename exists in the destination folder then the file overwrites the existing file.

### File Migrate New:

Select a source folder and a destination folder. The files in the source folder are CUT and COPIED (migrated) into the destination folder. This is not recursive, meaning the files within the child source folders are migrated, only the files directly in the source folder are migrated.

If the filename already exists in the destination folder then the file is migrated with a suffix determined by "Suffix". See appendix A for details.

### Single File Migrate New:

Select a source file and a destination folder. The source file is CUT and COPIED (migrated) into the destination folder. If the filename already exists in the destination folder then the file is migrated with a suffix determined by "suffix". See appendix A for details.

### File Migrate Overwrite:

Select a source folder and a destination folder. The files in the source folder are migrated into the destination folder. If the filename exists in the destination directory, then the source file is migrated IF AND ONLY IF the files differ in content. If the files have the same content, the file is not migrated.

### Single File Migrate Overwrite:

Select a source file and a destination folder. The source file is CUT and COPIED (migrated) into the destination folder. If the filename exists in the destination directory, then the source file overwrites the destination file and the source file is deleted.

### Folder Copy New

Select a source folder and a destination folder. Only the sub-folders in the source folder are copied into the destination folder. Note that all the contents within the source subfolders are also copied over.

If the foldername already exists in the destination folder then the folder is copied with a suffix determined by "Suffix". See appendix A for details.

### Single Folder Copy New

Select a source folder and a destination folder. The source folder and all its' contents are directly copied into the destination folder. If the foldername already exists in the destination folder then the folder is copied with a suffix determined by "Suffix". See appendix A.

Example:
Source = C://sourceFolder
Destination = C://destinationFolder
Result = C://destinationFolder/sourceFolder

### Folder Copy Overwrite

Select a source folder and a destination folder. Only the sub-folders in the source folder are copied into the destination folder. Note that all the contents within the source subfolders are also copied over.

If the foldername already exists in the destination folder then the folder is overwritten if their contents differ. Otherwise, if the folders are the same no overwriting is performed.

### Single Folder Copy Overwrite

Select a source folder and a destination folder. The source folder and all its' contents are directly copied into the destination folder. If the foldername already exists in the destination folder then the folder is overwritten.

### Directory Sync Overwrite

Select a source directory and a destination directory. All contents in the source directory are copied into the destination directory, including files and folders.

If a filename exists in the destination directory and the contents differ, then the file is overwritten. If a foldername exists in the destination directory and the contents differ, then the folder is overwritten.

Existing files and folders in the destination directory that are not in the source directory are maintained/not touched.

### Full Directory Sync

Select a source directory and a destination directory. All contents in the source directory are copied into the destination directory, including files and folders.

If a filename exists in the destination directory and the contents differ, then the file is overwritten. If a foldername exists in the destination directory and the contents differ, then the folder is overwritten.

WARNING: Any existing files/folders in the destination directory that are not in the source directory are DELETED.



## Appendix A

1. Basic:
   - Appends a numeric to the end of the newly copied file(s).
   - Example
     - Source File: README.txt
     - Destination Filename: README - 1.txt
2. Date:
   - Appends the date to the end of the newly copied file(s) with the format YYYY-MM-DD.
   - Example
     - Source File: Statement.pdf
     - Destination Filename: Statement 2020-02-17.pdf
3. Date-Time:
   - Appends the date and time to the end of the newly copied file(s) with the format YYYY-MM-DD HHhMMm.
   - Example:
     - Source File: changelog.txt
     - Destination Filename: changelog 2020-02-17 11h26m.txt
4. Timestamp:
   - Appends a timestamp to the end of the newly copied file(s) with the format YYYY-MM-DD HHhMMmSSs.
   - Example:
     - Source File: realtimelog.txt
     - Destination Filename: realtimelog 2020-02-17 11h26m07s.txt
5. Revision:
   - Appends a revision number to the end of the newly copied file(s) with the format REV - #
   - Exampe:
     - Source File: Design.sch
     - Destination Filename: Design - REV 0.sch
