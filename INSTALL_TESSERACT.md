# Installing Tesseract OCR for FreshTrack

## 📥 Windows Installation Guide

### Step 1: Download Tesseract Installer

For Windows, use the **UB-Mannheim** installer (recommended):

**Download Link**: https://github.com/UB-Mannheim/tesseract/wiki

1. Visit the link above
2. Look for the latest version (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)
3. Download the 64-bit installer
4. **Important**: Choose the installer that includes language packs!

### Step 2: Install Tesseract

1. **Run the installer** (double-click the `.exe` file)
2. **Important**: During installation, make sure to:
   - ✅ Check "Additional language data (download)" if you need Chinese/other languages
   - ✅ Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - ✅ Add to PATH if the installer offers this option

3. **Language Packs**: Since FreshTrack supports Chinese receipts, install:
   - ✅ English (`eng`)
   - ✅ Simplified Chinese (`chi_sim`)
   - ✅ Traditional Chinese (`chi_tra`) - optional

### Step 3: Verify Installation

Open a **new** Command Prompt or PowerShell window and run:

```bash
tesseract --version
```

You should see output like:
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.40 : libtiff 4.6.0 : zlib 1.3 : libwebp 1.3.2 : libopenjp2 2.5.0
```

### Step 4: Configure FreshTrack

The installation path needs to be configured in the OCR service.

**Default installation path**: `C:\Program Files\Tesseract-OCR\tesseract.exe`

I'll update the code to use this path automatically.

---

## 🐧 Linux Installation (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

## 🍎 macOS Installation

```bash
brew install tesseract tesseract-lang
```

---

## 🧪 Testing Tesseract

After installation, test with a simple command:

```bash
tesseract --list-langs
```

You should see:
```
List of available languages (3):
chi_sim
chi_tra
eng
```

---

## 📝 Notes

- **Chinese OCR**: For best results with Chinese receipts, `chi_sim` (Simplified Chinese) is essential
- **Installation Path**: The default Windows path is `C:\Program Files\Tesseract-OCR`
- **Environment Variables**: If Tesseract is not found, you may need to add it to your PATH manually

---

## ❓ Troubleshooting

### "tesseract not found" error

**Solution 1**: Add to PATH manually
1. Search "Environment Variables" in Windows
2. Edit "Path" under System Variables
3. Add: `C:\Program Files\Tesseract-OCR`
4. Restart Command Prompt

**Solution 2**: Update the OCR service configuration
The `ocr_service.py` file should have the path configured. I'll update it for you.

---

## 🚀 After Installation

Once Tesseract is installed:

1. **Restart** any open terminal/command prompt windows
2. **Restart** the FreshTrack API server:
   ```bash
   cd C:\Users\egeun\Documents\FreshTrack\backend
   venv\Scripts\python main.py
   ```
3. **Test** receipt upload through the web interface!

---

## ✅ Quick Installation Checklist

- [ ] Download Tesseract installer from UB-Mannheim
- [ ] Install with Chinese language pack (`chi_sim`)
- [ ] Verify with `tesseract --version`
- [ ] Check languages with `tesseract --list-langs`
- [ ] Restart API server
- [ ] Test receipt upload!

---

**Once installed, your receipt scanning will work perfectly!** 📸✨
