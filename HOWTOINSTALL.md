Here's the refined version of your instructions:

---

### 1. Download the Code

You have two options to get the code:

- **Using Git (Recommended):**  
  If you're familiar with Git, clone the repository by running the following command in your terminal or command prompt:

  ```bash
  git clone https://github.com/efe-codex/empire_bidder.git
  ```

- **Downloading as ZIP:**  
  If you're not comfortable with Git, you can download the latest version of the code from the [Releases page](https://github.com/efe-codex/empire_bidder/releases). Just click on the latest release, download the ZIP file provided there, and extract the contents to a folder on your computer.

### 2. Install Python

Make sure you have Python installed. I am using version 3.12.4. If you don't already have Python, follow these steps:

- Visit the [Python download page](https://www.python.org/downloads/).
- Download the installer for your operating system.
- Run the installer and follow the on-screen instructions.
- Be sure to check the option to add Python to your system PATH during installation.

If you're unsure how to do this, search for a tutorial on YouTube with the keyword "How to install Python."

### 3. Install Required Packages

Next, install the necessary Python packages using `pip`. Open a terminal or command prompt and run the following command:

```bash
pip install colorama pygsheets requests pandas python-socketio==4.6.1 python-engineio==3.14.2
```

**Important:**  
Empire uses Socket.IO version 2.x, so it's essential to install `python-socketio` version 4.x and `python-engineio` version 3.x for compatibility.

---
