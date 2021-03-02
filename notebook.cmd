@echo off

title jupyter @ logmlwip

call activate logml
call conda env list

setlocal
set PROJECT_ROOT=%cd%
set PYTHONPATH=%PYTHONPATH%;%cd%/src

call jupyter notebook
