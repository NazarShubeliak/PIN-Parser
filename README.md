# 📦 PIN Parser

A modular pipeline for downloading and parsing PIN invoices, with support for GUI and CLI execution.

---

## 🚀 Features

- Date-based invoice processing via GUI or CLI
- CustomTkinter GUI with integrated third-party date picker
- Threaded execution to keep the interface responsive
- Modular runners for weekly, monthly, and manual modes
- Clear separation of logic, UI, and third-party code
- Bilingual documentation for international onboarding

---

## 🖥️ GUI Mode

Launch the graphical interface to select a date range and run the pipeline manually:

```bash
python run.py --gui
```

## Run the pipeline in automated modes:
```bash
python run.py --week   # Weekly mode
python run.py --month  # Monthly mode
```
## 📁 Project Structure
```bash
root/
├── run.py                      # Unified entry point
├── gui/
│   ├── gui_runner.py           # GUI launcher
│   └── pin_gui.py              # PinGui class
├── runners/                    # CLI runners
├── parser/                     # Core logic
├── third_party/
│   └── ctk_date_picker/        # External widget
```

## 🧩 Third-Party Integration

CTkDatePicker is integrated from GitHub under the MIT license. See third_party/ctk_date_picker/INTEGRATION.md for details.

## 📚 Documentation

Each module and function includes docstrings in English. Configuration and onboarding instructions are available in both English and Ukrainian.

## 🛠 Requirements
```bash
pip install -r requirements.txt