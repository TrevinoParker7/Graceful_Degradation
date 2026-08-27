# Complete Beginner's Guide to GracefulOS (For Windows 11)

This guide is written for anyone who has never used a security OS or coding tool before. Just follow these steps in order.

---

## 💻 Step 1: Make Sure You Have Python Installed

1. Open your web browser and go to: **[https://www.python.org/downloads/](https://www.python.org/downloads/)**
2. Click the big yellow **"Download Python"** button.
3. Open the downloaded installer file.
4. ⚠️ **VERY IMPORTANT**: Before clicking install, look at the bottom of the installer window and **check the box that says:**
   > `☑ Add python.exe to PATH`
5. Click **"Install Now"** and wait for it to finish.

---

## 📥 Step 2: Download the Project

### Option A: The Fast Terminal Way (`git clone`)
Open PowerShell or Command Prompt and run:
```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd Graceful_Degradation
.\install.bat
.\start.bat
```
*(That's it! Your browser will open automatically)*

---

### Option B: The Web Browser Way (Download ZIP)
1. Go to the GitHub repository page.
2. Click the green **`<> Code`** button near the top right.
3. Click **`Download ZIP`**.
4. Right-click the downloaded `.zip` file → click **`Extract All...`** → click **`Extract`**.
5. Open the folder and double-click **`install.bat`**.

---

## ⚙️ Step 3: Run the 1-Click Installer

Inside the project folder, you will see a file named:
👉 **`install.bat`**

1. **Double-click `install.bat`**.
2. A black terminal window will open and automatically download the required files and set up your system.
3. When it is finished, you will see:
   ```text
   ======================================================================
     SUCCESS! GracefulOS is ready for your Windows 11 machine.
   ======================================================================
   Press any key to continue . . .
   ```
4. Press any key on your keyboard to close the window.

*(You only have to do this once!)*

---

## 🚀 Step 4: Start GracefulOS (1-Click)

Inside the project folder, find the file named:
👉 **`start.bat`**

1. **Double-click `start.bat`**.
2. A black terminal window will open to run the security engine.
3. **Within 2 seconds, your web browser will automatically open** to the GracefulOS Dashboard at:
   ```text
   http://127.0.0.1:7777
   ```

---

## 🎮 Step 5: How to See It in Action (Fun Test)

Once the dashboard is open in your browser:

1. Look at the top-right corner of the web page.
2. Click the **`⚡ Run Attack Demo`** button.
3. Watch the screen! You will see:
   - A simulated rogue AI agent try to hack the system.
   - The **Risk Score** jump up from `0` to `100 / 100`.
   - The status change to **`CONTAINED`** (Red alert).
   - Windows NT kernel physically terminate the rogue process and lock the folder.
   - The full step-by-step story appear in the **Incident Replay** tab!

---

## 🤖 Step 6: How to Connect Any AI Agent

If you or a developer write a Python script or AI assistant, route its actions through GracefulOS:

```python
import requests

# Send a safe request to read a file
response = requests.post("http://127.0.0.1:7777/api/v1/tools/invoke", json={
    "agent_id": "my-cool-agent",
    "tool_name": "read_file",
    "arguments": {"path": "README.md"}
})

print(response.json())
```

---

## 🛑 Step 7: How to Turn It Off

When you are done:
- Just close the black `start.bat` terminal window!
- Everything stops cleanly.
