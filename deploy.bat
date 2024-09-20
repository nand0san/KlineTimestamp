@echo off
setlocal enabledelayedexpansion

:: Ejecuta la generación del paquete fuente
python setup.py sdist

:: Obtiene el último archivo generado en el directorio dist
for /f "delims=" %%i in ('dir /b /o-d dist\*.tar.gz') do (
    set "latest_file=%%i"
    goto :break
)
:break

:: Sube el archivo más reciente a PyPI
python -m twine upload -r pypi "dist\!latest_file!"

:: Finaliza el script
endlocal
