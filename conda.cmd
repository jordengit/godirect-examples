set CONDA_ROOT_PREFIX=D:\miniforge3
set INSTALL_ENV_DIR=%CONDA_ROOT_PREFIX%\envs\veriner
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo ERROR: Miniconda hook not found. && goto end )
cmd