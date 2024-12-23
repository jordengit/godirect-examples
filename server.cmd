set CONDA_ROOT_PREFIX=%LOCALAPPDATA%\miniforge3
set INSTALL_ENV_DIR=%CONDA_ROOT_PREFIX%\envs\veriner
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo ERROR: Miniconda hook not found. && goto end )
cd python
fastapi dev apiserver.py
pause