set CONDA_ROOT_PREFIX=D:\miniforge3
set INSTALL_ENV_DIR=D:\miniforge3\envs\veniner
call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" || ( echo. && echo ERROR: Miniconda hook not found. && goto end )
cmd