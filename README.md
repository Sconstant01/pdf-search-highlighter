# PDF Search & Highlight Tool

A web-based application that searches PDFs in a shared folder for keywords, highlights matches, and extracts cost data.

## Features

- 🔍 Search for keywords/phrases across multiple PDFs
- 🎨 Highlight all instances of search terms on PDF pages
- 📊 Extract cost values from line items (uses first occurrence for average calculation)
- 📋 Display list of matching PDFs with page numbers
- 💰 Calculate average cost for matched line items
- 🌐 Web interface - accessible from any browser
- 👥 Multi-user access - no login required

## Requirements

- Python 3.8 or higher
- Windows, Mac, or Linux

## Installation

### Step 1: Install Python
Download and install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation

### Step 2: Download the Application
- Clone or download this repository to a folder on your computer
- Example: `C:\Users\YourUsername\pdf-search-tool`

### Step 3: Install Required Libraries
Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install flask pdfplumber pillow
```

## Setup

### Configure the PDF Folder Path

1. Open `app.py` in a text editor
2. Find this line (around line 10):
   ```python
   PDF_FOLDER = r"C:\Users\223146805.AEROAD\OneDrive - GE Aerospace\Desktop\Sourcing Quotes API"
   ```
3. Replace with your actual folder path if different
4. Save the file

## Running the Application

### On Windows:
1. Open Command Prompt
2. Navigate to your application folder:
   ```bash
   cd C:\Users\YourUsername\pdf-search-tool
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your web browser and go to: `http://localhost:5000`

### On Mac/Linux:
1. Open Terminal
2. Navigate to your application folder:
   ```bash
   cd /path/to/pdf-search-tool
   ```
3. Run the application:
   ```bash
   python3 app.py
   ```
4. Open your web browser and go to: `http://localhost:5000`

## Usage

1. **Enter Search Terms**: Type the keyword or phrase you want to find
2. **Click Search**: The app will search all PDFs in the folder
3. **View Results**: 
   - See list of PDFs with matching page numbers
   - View average cost for matched line items
   - Click on a PDF to view it with highlights
4. **Highlighted Text**: All instances of your search term will be highlighted in yellow
5. **Cost Calculation**: Only the first occurrence of each line item's cost is used for the average

## Sharing with Others

### On Your Local Network:
1. Find your computer's IP address:
   - Windows: Open Command Prompt and type `ipconfig`, look for "IPv4 Address"
   - Mac/Linux: Open Terminal and type `ifconfig`
2. Share the IP address with others (e.g., `192.168.1.100`)
3. They can access the app at: `http://192.168.1.100:5000`

### Requirements for Others:
- Must be on the same network
- Must have access to the shared folder (same network access)

## Troubleshooting

**"ModuleNotFoundError: No module named 'flask'"**
- Run: `pip install flask pdfplumber pillow`

**"Cannot find folder"**
- Check the PDF folder path in `app.py`
- Make sure the folder exists and contains PDF files

**"Address already in use"**
- Another app is using port 5000
- Close other applications or edit `app.py` to use a different port

**PDFs not showing highlights**
- Make sure PDFs are in the correct folder
- Try restarting the application

## Support

For issues or questions, check the troubleshooting section above.
