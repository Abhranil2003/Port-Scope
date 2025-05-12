# 🔒 Port Scope

Port Scope is a powerful and flexible port scanning tool designed to detect open ports and alert users of any potential unauthorized entries on a target system or network. It combines the reliability of Nmap with multi-format reporting capabilities including CSV, PDF, HTML, JSON, and plain text — making it easier to analyze and document scan results.

Designed for security professionals, students, and developers who want a modular, customizable, and CLI-driven tool to perform basic reconnaissance and scanning tasks, Port Scope empowers users with control, clarity, and actionable insights into their network security posture.

---

## 🚀 Features

- 🔍 Focused on **Port Scanning** and **alerts for unauthorized access detection**
- 📄 Generates reports in **PDF**, **HTML**, **CSV**, **JSON** and **Text** formats
- 🕓 **Schedule scans** for delayed or repeated execution
- 📦 Clean, modular structure for easy customization and extension
- ⚙️ Auto-detects Nmap and other dependencies, provides graceful fallbacks if missing
- ✅ Friendly CLI interface with confirmation prompts and detailed scan logs
- 🧪 Supports testing with mock output, raw Nmap data saving, and sample report generation

---

## 🧱 Directory Structure

```
project-root/
│
├── main.py                              # Entry point
│
├── scanner.py                           # Core scanning engine
│
├── cli.py                               # Command-line interface for initiating scans and generating reports
│   
├── scheduler.py                         # Scan scheduling logic
│   
├── utils.py                             # Helper functions
│   
├── parsers/                             # Nmap & web scanner output parser
│   ├── nmap_parser.py
│   └──_init_.py
│     
├── reporter/                            # All report generators
│   ├── html_reporter.py
│   ├── pdf_reporter.py
│   ├── csv_reporter.py
│   ├── json_reporter.py
│   ├── text_reporter.py
│   ├── _init_.py
│   ├── assets/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│   │   └── report_template.html
│
├── tests/                               # All test files
│   ├── test_reporters/                  # Output directory for reports
│   │   ├── _init_.py
│   │   ├── test_csv_reporter.py
│   │   ├── test_html_reporter.py
│   │   ├── test_json_reporter.py
│   │   ├── test_pdf_reporter.py
│   │   └── test_text_reporter.py
│   ├── _init_.py
│   ├── test_cli.py
│   ├── test_parser.py
│   ├── test_scanner.py
│   ├── test_scheduler.py
│   └── test_utils.py
│        
├── logs/ 
│        
├── sample_reports/ 
│  
├── docs/
│   └── CONTRIBUTING
│
├── requirements.txt
│
├──SECURITY.md
│
├──CODE_OF_CONDUCT.md
│
└── README.md
```

---

## 🛠️ Prerequisites

- **Python 3.7+**

- **Tools:**
  - [`nmap`](https://nmap.org/) must be installed and added to your system’s PATH for port scanning to work.
  - [`Playwright`](https://playwright.dev/python/) is used for high-fidelity PDF report generation (included in `requirements.txt`).

> ⚠️ After installing dependencies with:
> 
> ```bash
> pip install -r requirements.txt
> ```
> 
> Run the following once to install Playwright browser binaries (like Chromium):
> 
> ```bash
> python -m playwright install
> ```

---

## 📦 Installation

```bash
git clone https://github.com/Abhranil2003/Port-Scope.git
cd Port-Scope
pip install -r requirements.txt
python -m playwright install
playwright install winldd  # ✅ Required on Windows for PDF generation
```

---

## ⚙️ Configuration

- Edit templates in `/reporter/templates/report_template.html` for custom branding
- Edit templates' style in `/reporter/assets/script.js` and `/reporter/assets/style.css` for custom styling in the template
- Modify `test_reporters/` path in `utils.py` if you want a different output directory

---

## 🧪 Usage

```bash
# 🔍 Full scan (default) and HTML output
python main.py example.com -o html

# 🚀 Quick scan with CSV output
python main.py example.com -o csv --scan-type quick

# 🧠 OS detection scan with JSON output
python main.py example.com -o json --scan-type os

# 🛠️ Custom Nmap scan using user-defined flags
python main.py example.com --scan-type custom --custom-options "-sS -Pn -T4" -o pdf

# 🌐 Web scan using HTTP(S) target and generate HTML report
python main.py https://example.com --scan-type web -o html

# 🎯 Scan specific ports and output to multiple formats
python main.py 192.168.0.1 -p 22,80,443 -o csv pdf

# 📄 Save raw Nmap output for forensics
python main.py scanme.nmap.org -o text --raw

# ⏱️ Delayed Scan (starts after 30 seconds) [CLI only]
python cli.py example.com quick -r html --schedule --delay 30

# 🔁 Repeated Scan (3 times, 60 seconds apart) [CLI only]
python cli.py example.com quick -r csv --repeated --interval 60 --repetitions 3

```

---

## 💡 Examples

### Sample CLI Output

```text
[INFO] Starting scan...
[INFO] Scan completed in 12.5 seconds
[INFO] Generating HTML report...
✅ Report saved to test_reporters/scan_report_20250429_133212.html
```

### 📸 Report Preview Of A Sample HTML Output
![sample](https://i.postimg.cc/1XFttmQC/sample.png)

---

## 🧪 Testing

- Test JSON/Text output with test values using `scanner.py`
- Use mocked responses for development if nmap is not available

---

## 🤝 Contributing

1. Fork this repo
2. Create your branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a Pull Request

---

## 💬 Feedback

We highly appreciate your input to make **Port Scope** better. Whether you found a bug, have a suggestion, or just want to share how you're using it—we'd love to hear from you. Feel free to open an [issue](https://github.com/Abhranil2003/Port-Scope/issues) or reach out via email:  
📧 abhranilpoddar18@gmail.com

### ✉️ How to Give Feedback

We welcome suggestions, bug reports, or any thoughts you may have! Here’s how you can reach us:

- 🐛 **Found a bug?** [Open an issue](https://github.com/Abhranil2003/port-scope/issues) on GitHub with details and steps to reproduce.
- 🌟 **Have a feature request?** Create a [feature request issue](https://github.com/Abhranil2003/port-scope/issues/new?labels=enhancement).
- 📬 **General feedback or questions?** Start a [discussion](https://github.com/Abhranil2003/port-scope/discussions).
- 🙌 **Want to contribute?** Check out our [Contributing Guide](#CONTRIBUTING).

### 🗣️ Common Feedback

- 💡 "The CLI is very intuitive and easy to use."
- 🧩 "Modular structure makes it really easy to extend."
- 📊 "Having multiple report formats is extremely helpful for documentation."
- ⏱️ "The scheduling feature is perfect for repeated scans during monitoring windows."


---

## 📄 License

This project is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for more information.

---

## 🙏 Acknowledgements

- [Nmap](https://nmap.org/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [pdfkit](https://pypi.org/project/pdfkit/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- Inspiration from OWASP tools and open-source scanners

---

Thank you ❤️!