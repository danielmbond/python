@ECHO OFF
SET PY = "C:\Program Files\Python36\python.exe"
SET SCRIPT = "C:\Users\Daniel\Documents\Scripts\Python\sabnzbd\delete-old-episodes.py"
%PY % %SCRIPT % %*
ECHO Script Complete
