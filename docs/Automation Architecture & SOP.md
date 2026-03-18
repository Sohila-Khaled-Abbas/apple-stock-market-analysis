# **Data Pipeline Automation SOP**

## **Option 1: The Brittle Approach (Local Automation via Windows Task Scheduler)**

This approach binds your data pipeline to your local hardware. If your machine is off at 18:00, the data does not update.

### **Step 1: Circumvent the Anaconda Environment Trap**

Task Scheduler cannot activate Conda environments natively. You must create a batch file (.bat) to initialize the environment before executing the script.

1. Open Notepad.  
2. Write the following commands, adjusting the paths to match your exact directory structure:  
   @echo off  
   :: Activate the Anaconda environment  
   call "C:\\Users\\HELAL\\anaconda3\\Scripts\\activate.bat" myenvironment

   :: Execute the Python script  
   python "C:\\path\\to\\your\\update\_apple\_stock.py"

   :: Optional: log the output to verify execution  
   echo Ran update at %date% %time% \>\> "C:\\path\\to\\your\\execution\_log.txt"

3. Save the file as run\_pipeline.bat.

### **Step 2: Configure Windows Task Scheduler**

1. Open **Task Scheduler** in Windows.  
2. Click **Create Basic Task...** in the right pane.  
3. Name it AAPL\_Data\_Pipeline.  
4. Trigger: Choose **Daily**. Set the time to **18:00:00** (after the US market closes).  
5. Action: Choose **Start a program**.  
6. Program/script: Browse and select the run\_pipeline.bat file you created in Step 1\.  
7. Finish the setup.  
8. *Critical Step:* Right-click the newly created task, go to **Properties**, and check **"Run whether user is logged on or not"**. This requires entering your Windows password and ensures the script runs even if the screen is locked.

## **Option 2: The Robust Approach (Cloud Automation)**

A true automated pipeline decouples the execution from personal hardware. Since yfinance is a free API, this script should run in the cloud (e.g., GitHub Actions, AWS Lambda).

*Counter-argument to your current setup:* You are maintaining a local MySQL database. If you migrate your MySQL database to a managed cloud provider (like AWS RDS or PlanetScale), you can use GitHub Actions to run your Python script entirely in the cloud for free.

### **GitHub Actions Implementation (If MySQL is accessible via internet)**

1. Push your update\_apple\_stock.py and a requirements.txt to a GitHub repository.  
2. Create a directory .github/workflows/ and add a file named pipeline.yml.  
3. Use the following YAML to execute the script every weekday at 22:00 UTC:

name: AAPL Daily Data Ingestion  
on:  
  schedule:  
    \- cron: '0 22 \* \* 1-5' \# Runs at 22:00 UTC, Monday through Friday  
  workflow\_dispatch: \# Allows manual trigger

jobs:  
  update-db:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v3  
      \- name: Set up Python  
        uses: actions/setup-python@v4  
        with:  
          python-version: '3.10'  
      \- name: Install dependencies  
        run: pip install \-r requirements.txt  
      \- name: Run ingestion script  
        env:  
          DB\_PASSWORD: ${{ secrets.DB\_PASSWORD }} \# Stored securely in GitHub Secrets  
        run: python update\_apple\_stock.py

## **Step 3: Automating the Power BI Refresh**

Updating the MySQL database is only half the pipeline. Power BI Service (the cloud dashboard) will not automatically detect changes in your local MySQL database.

1. **Install the On-premises Data Gateway:** Download and install the gateway from Microsoft on the same machine hosting the MySQL database.  
2. **Configure the Gateway:** Sign in with your Power BI credentials. This creates a secure bridge between your local MySQL port (3306) and the Power BI cloud.  
3. **Map the Data Source:** In Power BI Service, go to Settings \-\> Manage gateways. Add your MySQL database credentials.  
4. **Schedule the Refresh:** Go to your dataset settings in Power BI Service. Enable "Scheduled refresh" and set it to trigger at **18:30** (giving your Python script 30 minutes to finish its execution and write to the database).

### **The Logical Bottleneck:**

If you use Option 1 (Local Python) \+ Local MySQL \+ Local Gateway, your PC has now become a server. It must remain powered on and connected to the internet 24/7/365, otherwise the entire chain fails.