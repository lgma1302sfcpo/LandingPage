@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   CRIAR NOVO CLIENTE - LANDING PAGE
echo ========================================
echo.

set /p SLUG="Slug do cliente (ex: salao-maria): "
set /p NOME="Nome do negocio (ex: Salao Maria): "

if "%SLUG%"=="" (
    echo Erro: Slug e obrigatorio!
    pause
    exit /b 1
)

set PASTA=clientes\%SLUG%

if exist "%PASTA%" (
    echo.
    echo Erro: A pasta %PASTA% ja existe!
    pause
    exit /b 1
)

echo.
echo Criando pasta %PASTA%...
mkdir "%PASTA%"

echo Copiando template...
copy "clientes\esmalteria-brandao\index.html" "%PASTA%\index.html" >nul

echo.
echo ========================================
echo   CLIENTE CRIADO COM SUCESSO!
echo ========================================
echo.
echo Pasta: %PASTA%
echo.
echo PROXIMOS PASSOS:
echo 1. Edite o arquivo %PASTA%\index.html
echo 2. Substitua os dados (nome, endereco, WhatsApp, etc)
echo 3. Troque as imagens do Unsplash pelas do cliente
echo 4. Execute: vercel --prod
echo 5. Envie o link: seusite.vercel.app/%SLUG%
echo.
pause
