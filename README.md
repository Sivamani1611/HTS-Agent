# 🌐 HTS AI Agent - Enhanced Trade Intelligence Platform
_Professional Trade Intelligence & Duty Calculation System for the U.S. Harmonized Tariff Schedule (HTS)_

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

</div>

---

## 📋 Table of Contents

1. [What Is HTS AI Agent?](#what-is-hts-ai-agent)  
2. [Why Choose This Platform?](#why-choose-this-platform)  
3. [Key Features](#key-features)  
4. [📂 Current Project Structure](#current-project-structure)  
5. [⚙️ Quick Setup](#quick-setup)  
6. [🚀 Usage Guide](#usage-guide)  
7. [💻 CLI Enhanced Features](#cli-enhanced-features)
8. [📊 Recent Enhancements](#recent-enhancements)

---

## 📌 What Is HTS AI Agent?

**HTS AI Agent** is a professional-grade Python platform designed for trade professionals, importers, and supply-chain teams to:

- **Calculate import duties & landed costs** with precision
- **Process batch calculations** for multiple shipments  
- **Search and compare HTS codes** with advanced analytics
- **Export data** in multiple formats (JSON, CSV)
- **Interactive trade assistance** via enhanced CLI and web interface

_Available through both advanced CLI tools and a comprehensive web dashboard._

---

## 💖 Why Choose This Platform?

- **🧹 Clean & Organized**: Streamlined codebase with only essential, working applications
- **🚀 Enhanced Features**: 40+ web features and 18+ new CLI capabilities  
- **💻 Multiple Interfaces**: Web app, enhanced CLI, interactive CLI, and project management tools
- **📊 Professional Tools**: Batch processing, data export, search, comparison, and analytics
- **⚡ Easy Access**: Multiple launch methods for different user preferences

---

## ✨ Key Features

### 🌐 **Web Applications**
- **Ultimate Web App** - Full-featured with 40+ capabilities including dashboard, calculators, batch processing, analytics
- **Working Web App** - Stable backup version with core functionality

### 💻 **Enhanced CLI Tools**
- **Advanced CLI** - Command-line interface with 10+ new features (search, compare, batch, export, stats)
- **Interactive CLI** - Chat-based interface with enhanced capabilities

### ⚙️ **Management Tools**
- **Simple Launcher** - Easy access to all applications
- **Project Manager** - Comprehensive project management console
- **Status Monitoring** - Real-time application and environment status

---

## 📂 Current Project Structure

```
📦 HTS-Agent-main/
├── 🌐 Web Applications
│   ├── app_ultimate.py      # 🏆 Main enhanced app (70KB, 1876 lines)
│   └── app_working.py       # 🔧 Stable backup (24KB, 558 lines)
│
├── 💻 CLI Applications  
│   ├── main_fixed.py        # 🚀 Enhanced CLI (19KB, 485 lines)
│   └── cli_simple.py        # 🗣️ Interactive CLI (21KB, 501 lines)
│
├── ⚙️ Management Tools
│   ├── launch_hts.py        # 🚀 Simple launcher (11KB, 285 lines)
│   └── manage_project.py    # 🔧 Project manager (16KB, 439 lines)
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── PROJECT_CLEANUP_SUMMARY.md  # Recent cleanup documentation  
│   └── FINAL_STATUS.md             # Comprehensive status report
│
├── 📦 Dependencies
│   ├── requirements.txt        # Main dependencies
│   ├── requirements_basic.txt  # Basic dependencies
│   └── environment.yml         # Conda environment
│
└── 📁 Supporting Directories
    ├── hts_agent_env/         # Virtual environment
    ├── config/                # Configuration files
    ├── tools/                 # Additional tools
    ├── data/                  # Data files
    ├── logs/                  # Application logs
    └── [tests/, scripts/, models/, agent/]
```

---

## ⚙️ Quick Setup

### 1. **Clone and Navigate**
```bash
git clone <repository-url>
cd HTS-Agent-main
```

### 2. **Set Up Environment** 
```bash
# Create virtual environment
python -m venv hts_agent_env

# Activate environment (Windows)
hts_agent_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Verify Installation**
```bash
python launch_hts.py --status
```

---

## 🚀 Usage Guide

### **🌟 Recommended: Simple Launcher**
```bash
# Interactive menu
python launch_hts.py

# Direct launches
python launch_hts.py --web ultimate     # Ultimate web app
python launch_hts.py --web working      # Working web app  
python launch_hts.py --cli enhanced     # Enhanced CLI
python launch_hts.py --cli interactive  # Interactive CLI
python launch_hts.py --status           # Project status
```

### **🌐 Web Applications**
```bash
# Ultimate web app (recommended)
streamlit run app_ultimate.py

# Working web app (stable backup)
streamlit run app_working.py
```

### **💻 CLI Applications**
```bash
# Enhanced CLI with advanced features
python main_fixed.py --chat             # Interactive mode
python main_fixed.py --stats            # Database statistics
python main_fixed.py --search "cattle"  # Search HTS codes

# Interactive CLI
python cli_simple.py                    # Chat-based interface
```

### **⚙️ Project Management**
```bash
python manage_project.py               # Management console
python manage_project.py --run-app ultimate
python manage_project.py --run-cli enhanced
```

---

## 💻 CLI Enhanced Features

### **🔍 Advanced Search & Analysis**
```bash
python main_fixed.py --search "cattle"        # Search HTS codes
python main_fixed.py --compare 0101.30.00.00 0102.21.00.00  # Compare rates  
python main_fixed.py --stats                  # Database statistics
```

### **📊 Batch Processing**
```bash
python main_fixed.py --template               # Generate CSV template
python main_fixed.py --batch mydata.csv       # Process batch calculations
```

### **💾 Data Export**
```bash
python main_fixed.py --export json            # Export database as JSON
python main_fixed.py --export csv             # Export database as CSV
```

### **🎮 Enhanced Interactive Mode**
```bash
python main_fixed.py --chat                   # Interactive chat with new commands

# Available in chat mode:
# search <keyword>, compare <codes>, stats, template, export <format>
```

---

## 📊 Recent Enhancements

### **🧹 Project Cleanup (Completed)**
- ✅ **Removed 7 unnecessary Streamlit apps** (87% reduction in app files)
- ✅ **Eliminated broken/problematic files** 
- ✅ **Streamlined to 2 working, tested applications**

### **🚀 CLI Enhancements (18+ New Features)**
- ✅ **Advanced search capabilities** - Find HTS codes by keyword
- ✅ **Multi-code comparison** - Compare duty rates across codes
- ✅ **Database analytics** - Comprehensive statistics and insights
- ✅ **Batch processing** - CSV template generation and bulk calculations
- ✅ **Data export** - JSON and CSV export functionality
- ✅ **Enhanced interactive modes** - Improved chat interfaces

### **⚙️ Management Improvements**
- ✅ **Simple launcher script** - Easy access to all applications
- ✅ **Updated project manager** - Reflects current clean structure
- ✅ **Status monitoring** - Real-time application and environment status
- ✅ **Professional documentation** - Comprehensive usage guides

---

## 🎯 Getting Started Examples

### **Quick Duty Calculation**
```bash
python main_fixed.py --calc 0101.30.00.00 10000 500 100
```

### **Search for Products**
```bash
python main_fixed.py --search "cattle"
```

### **Compare Rates**
```bash
python main_fixed.py --compare 0101.30.00.00 0102.21.00.00
```

### **Interactive Mode**
```bash
python main_fixed.py --chat
> search beef
> stats  
> export json
```

---

## 📞 Support & Documentation

- **📖 Comprehensive Docs**: `PROJECT_CLEANUP_SUMMARY.md` - Detailed cleanup and enhancement summary
- **📊 Status Report**: `FINAL_STATUS.md` - Complete feature documentation and status
- **🚀 Quick Help**: `python launch_hts.py --help` - Command-line help
- **💬 Interactive Help**: Use chat mode commands for real-time assistance

---

## 🏆 Current Status

**✅ Ready for Production**
- All applications tested and working
- Enhanced features fully functional  
- Clean, maintainable codebase
- Professional user experience
- Multiple access methods available

**🎉 The HTS AI Agent is now a clean, professional, and feature-rich trade intelligence platform!**

---

*HTS AI Agent - Enhanced Trade Intelligence Platform*  
*Status: ✅ OPTIMIZED*
 