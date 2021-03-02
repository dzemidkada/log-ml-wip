@echo off

call activate logml
call conda env list
call conda env update -f environment.yml
