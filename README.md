# 🎡 WonderWorld

WonderWorld allows users to explore attractions, plan a personalised itinerary, book tickets and receive confirmation emails.

## 1. Prerequisites
Open command terminal by clicking ' Ctrl + ` ' 
or 
Go to View > Terminal

Install the following before starting:

- [Python](https://www.python.org/downloads/) — use the latest available Python **3.13.x** release for consistency with the project. Newer major/minor versions have not been verified.

Open a PowerShell terminal and check:

py -3.13 --version
git --version

Python should report `Python 3.13.x`

## 2. Create a virtual environment to start the website

Type in this command:
```
.\.venv\Scripts\Activate.ps1

```

The terminal should now show `(.venv)` before the folder path.

### PowerShell security / execution policy error

If PowerShell reports that running scripts is disabled, you can try this command:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  

Then run this again: 
.\.venv\Scripts\Activate.ps1

This does not permanently change the computer's execution policy and does not require administrator privileges under normal circumstances. Do not disable antivirus or bypass organisation-managed security policies.

Alternatively, no policy change or activation is required if you run the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## 4. Configure email functionality (first time only)

The itinerary and ticket receipt features use Gmail SMTP. Each teammate should configure their own Gmail account and app password locally.

### 4.1 Generate a Google app password

1. Visit [Google Account Security](https://myaccount.google.com/security).
2. Enable **2-Step Verification** if it is not already enabled.
3. Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
4. Create an app password named `WonderWorld`.
5. Copy the generated 16-character password.

Use the generated **app password**, not your normal Gmail password. Some managed accounts or security configurations do not support app passwords; use an eligible account or contact the maintainer if unavailable.

### 4.2 Create the secrets file

In the project root, create a folder called `.streamlit` if it does not already exist. Inside it, create a file called `secrets.toml`.

```text
pythonProjectGroup6/
├── .streamlit/
│   └── secrets.toml
├── .venv/
├── assets/
├── database/
├── pages/
├── src/
├── app.py
├── requirements.txt
└── README.md
```

Paste the following into `secrets.toml` and replace the placeholders with your own credentials:

```toml
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_APP_PASSWORD = "your-16-character-app-password"
```

Save the file. Restart Streamlit if it was already running.

**Important:** Never share your app password, include it in screenshots, or upload `secrets.toml` to GitHub. Ensure `.streamlit/secrets.toml` and `.venv/` are listed in the project's `.gitignore`. If a credential is exposed, revoke the app password in your Google account and generate a new one.

## 5. Run the website

Every time you open a new terminal, activate the virtual environment again:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Streamlit should open the website automatically. If it does not, open the Local URL printed in the terminal (usually http://localhost:8501).

Keep the terminal running while using the website. To stop the application, press `Ctrl + C` in the terminal.

## 6. Retrieve the latest updates from GitHub
run:

```powershell
git pull --ff-only
```

Activate your environment, install any updated dependencies and restart the website:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Your personal secrets file should remain unchanged as long as it is ignored and not tracked by Git.

## 7. Repository rules — pull only

To prevent accidental changes to the shared project, teammates should use GitHub to retrieve updates only.

- Do NOT use `git add`, `git commit`, `git push` or force-push commands.
- Do NOT use VS Code's Commit, Push, Publish Branch or Sync Changes buttons.
- Do NOT edit shared source files unless instructed by the project maintainer.
- Do NOT use `git reset --hard` or `git clean` to resolve problems.
- Report bugs or suggested improvements to the project maintainer instead.

These instructions are a team workflow, not a technical access restriction. The repository owner should grant read-only access where supported if teammates must be prevented from pushing changes.

## 8. Troubleshooting

| Problem | Solution |
| --- | --- |
| Python is not recognised | Install Python 3.13, check PATH and restart VS Code. |
| Incorrect Python version | Run `py -3.13 --version` and select the `.venv` interpreter. |
| Script execution is disabled | Follow Section 3 or use the virtual environment's Python directly. |
| `ModuleNotFoundError` | Activate `.venv` and run `python -m pip install -r requirements.txt`. |
| `streamlit` is not recognised | Use `python -m streamlit run app.py` instead. |
| `st.logo`, `st.Page` or `st.navigation` is missing | Check the interpreter and installed Streamlit version. Reinstall the project's specified dependencies. |
| `app.py` does not exist | Make sure the terminal is in the project root. |
| Secrets file not found | Check that `.streamlit/secrets.toml` exists and is not named `secrets.toml.txt`. Restart the app. |
| Email authentication fails | Verify the Gmail address and app password, not the normal account password. |
| Email connection times out | Check internet access and whether the network permits Gmail SMTP on port 587. Do not bypass network security controls. |
| Git pull fails or reports conflicts | Stop and contact the project maintainer. Do not force the pull or reset the repository. |
| Port 8501 is already in use | Open the URL printed by Streamlit or run `python -m streamlit run app.py --server.port 8502`. |

## 9. Overall quick reference 

Once initial setup is complete, the usual workflow is:

```powershell
git status
git pull --ff-only
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
---

