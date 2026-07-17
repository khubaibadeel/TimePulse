@echo off
setlocal
cd /d "%~dp0"

where git >nul 2>nul || (
  echo Git is not installed or not available on PATH.
  exit /b 1
)

if not exist .git (
  git init || exit /b 1
)

git add .
git diff --cached --quiet && (
  echo No staged changes to commit.
) || (
  set /p COMMIT_MESSAGE=Commit message [Prepare TimePulse repository]: 
  if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Prepare TimePulse repository"
  git commit -m "%COMMIT_MESSAGE%" || exit /b 1
)

git branch -M main
git remote get-url origin >nul 2>nul || (
  set /p REPO_URL=Enter the GitHub repository URL: 
  if "%REPO_URL%"=="" (
    echo Repository URL is required.
    exit /b 1
  )
  git remote add origin "%REPO_URL%" || exit /b 1
)

git push -u origin main
endlocal
