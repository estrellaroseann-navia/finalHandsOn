@echo off
setlocal

start "CRUD API" cmd /k "python API_final.py" 

:main
curl http://127.0.0.1:5000/

choice /c 1234e /N

if %ERRORLEVEL% == 1 (
    goto create
)
if %ERRORLEVEL% == 2 (
    goto retrieve
)
if %ERRORLEVEL% == 3 (
    goto update
)
if %ERRORLEVEL% == 4 (
    goto delete
)
if %ERRORLEVEL% =  = 5 (
    goto end 
)
goto end

:create
cls
echo "[CREATE DATA]"
set /p "first_name = Input first name: "
set /p "last_name = Input last name: "
set /p "gender = Input gender: "
set /p "password = Input password: "

if "%first_name%" == ""(
    echo First Name cannot be empty!
    pause
    goto create
)
if "%last_name%" == ""(
    echo Last Name cannot be empty!
    pause
    goto create
)
if "%gender%" == ""(
    echo Gender cannot be empty!
    pause
    goto create
)
if "%password%" == ""(
    echo Password cannot be empty!
    pause
    goto create
)

set "json_format"={\"first_name\":\"%first_name%\", \"last_name\":\"%last_name%\", \"gender\":\"%gender%\", \"password\":\"%password%\",}

curl -X POST -H "Content-Type: application/json" -d "%json_format%" http://127.0.0.1:5000/costumers
pause
echo Do you want to create another data for the Database?
choice /c yn 
if %ERRORLEVEL% == 1 goto main
if %ERRORLEVEL% == 2 goto create

:retrieve
cls
echo "[RETRIEVE DATA]"
echo [1] All User Detail/s
echo [2] Search User Detail/s (by ID)

choice /c 12 /N

if %ERRORLEVEL% == 1 goto showall
if %ERRORLEVEL% == 2 goto search

:showall
echo "[FORMAT]"
echo [1] JSON
echo [2] XML 

choice /c 12 /N

if %ERRORLEVEL% == 1 (
    curl http://127.0.0.1:5000/user_details
    pause
    goto retri_end
)
if %ERRORLEVEL% == 2 (
    curl http://127.0.0.1:5000/user_details?format=xml
    goto retri_end
)

:search_byID
set /p "search_id = Input User ID: "

if "%search_id%" == "" (
    echo "User ID cannot be empty!"
    pause
    goto search_byID
)

set /a valid_searchid = %search_id%
if %search_id% EQU %valid_searchid% (
    goto user_search
) else (
    echo Invalid User Id, please check!
    pause
    goto search_byID
)

:user_search
echo "[FORMAT]"
echo [1] JSON
echo [2] XML 

choice /c 12 /N
if %ERRORLEVEL% == 1 (
    curl -X GET http:// 127.0.0.1:5000/user_details/%search_id%
    pause 
    goto retri_end
)
if %ERRORLEVEL% == 2 (
    curl -X GET http://127.0.0.1:5000/user_details/%search_id%?format=xml
    pause
    goto retri_end
)

:retri_end
echo Do you want to retrieve some user detail/s again?

choice /c yn
if %ERRORLEVEL% == 1 goto retrieve
if %ERRORLEVEL% == 2 goto main

:update
set /p "update_id = Input User ID: "

if "%update_id%" == "" (
    echo "User ID cannot be empty!"
    pause
    goto update_byID
)

set /a valid_updateid = %update_id%
if %update_id% EQU %valid_updateid% (
    goto update_check
) else (
    echo Invalid User Id, please check!
    pause
    goto update
)

:update_check
curl -X GET http://127.0.0.1:5000/user_details/%update_id%

echo Do you want to proceed?

choice /c yn
if %ERRORLEVEL% == 1 goto update_details
if %ERRORLEVEL% == 2 goto update

:update_details
echo "[Input New User Detail/s]"
set /p "first_name = Input first name: "
set /p "last_name = Input last name: "
set /p "gender = Input gender: "
set /p "password = Input password: "

if "%first_name%" == ""(
    echo First Name cannot be empty!
    pause
    goto create
)
if "%last_name%" == ""(
    echo Last Name cannot be empty!
    pause
    goto create
)
if "%gender%" == ""(
    echo Gender cannot be empty!
    pause
    goto create
)
if "%password%" == ""(
    echo Password cannot be empty!
    pause
    goto create
)

set "json_format"={\"first_name\":\"%first_name%\", \"last_name\":\"%last_name%\", \"gender\":\"%gender%\", \"password\":\"%password%\",}

curl -X PUT -H "Content-Type: application /json _data"  -d "%json_data%" http://127.0.0.1:5000/user_details/%update_id%
pause
echo Do you want to update another USER DETAILS?

choice /c yn
if %ERRORLEVEL% == 1 goto update
if %ERRORLEVEL% == 2 goto main

:delete
set /p "delete_id = Input User ID: "

if "%delete_id%" == "" (
    echo "User ID cannot be empty!"
    pause
    goto delete
)

set /a valid_deleteid = %delete_id%
if %delete_id% EQU %valid_deleteid% (
    goto delete_check
) else (
    echo Invalid User Id, please check!
    pause
    goto delete
)

:delete_check
curl -X GET http://127.0.0.1:5000/user_details/%delete_id%

echo Do you wan to proceed?
choice /c yn
if %ERRORLEVEL% == 1 goto delete_user
if %ERRORLEVEL% == 2 goto delete

:delete_user
curl -X DELETE http://127.0.0.1:5000/user_details/%delete_id%
pause

echo Do you want to DELETE another user details?
choice /c yn
if %ERRORLEVEL% == 1 goto delete
if %ERRORLEVEL% == 2 goto main

:end
echo Thank You!