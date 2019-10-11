cd %~d0
cd %cd%

cd redis
start redis-server.exe redis25000.conf

cd ..
title gamexxy
python apptest.py