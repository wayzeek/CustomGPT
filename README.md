# 🤖 CustomGPT - Chat with your Data 📚 

CustomGPT is a sophisticated, multilingual chatbot platform designed to streamline the extraction, processing, and interaction with text data from PDF documents. Leveraging advanced NLP and machine learning models, it enables rich, interactive communication across multiple languages, making it ideal for businesses and educational institutions dealing with diverse document formats.

## 📚 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## 📖 Introduction

CustomGPT harnesses the power of conversational AI to enhance the way organizations handle document-based information. By automatically extracting and analyzing text from PDFs and facilitating dynamic interactions through its chatbot interface, CustomGPT transforms static data into actionable insights. This integration of document processing with advanced dialogue systems offers a unique solution that significantly boosts productivity and user engagement.

### Screenshot
![image](https://github.com/wayzeek/CustomGPT/assets/112975047/4b5da2d6-a2ed-4043-965b-e603c493a5e8)



## ✨ Features

- **PDF Text Extraction**: Efficiently extracts text from PDFs, handling multiple layouts and formats.
- **Advanced Text Processing**: Employs custom splitters and robust language detection to ensure accurate text analysis.
- **Multilingual Support**: Supports interaction in multiple languages with dedicated models:
  - **English** 🇬🇧
  - **Spanish** 🇪🇸
  - **French** 🇫🇷
  - **German** 🇩🇪
  - **Italian** 🇮🇹
  - **Ukrainian** 🇺🇦
  - **Russian** 🇷🇺
  - **Chinese** 🇨🇳
  - **Japanese** 🇯🇵
- **Interactive User Interface**: Offers a user-friendly command-line interface that may evolve into a more graphical interface.

## 🚀 Getting Started

### ⚙️ Installation
- **Step 1:** clone the repo
```bash
git clone https://github.com/wayzeek/CustomGPT.git
```
- **Step 2:** navigate to the directory
```bash
cd CustomGPT
```
- **Step 3:** install dependencies
```bash
bash install.sh
```
- **Step 4:** move to virtual environment
```bash
source .venv/bin/activate
```
- **Step 5:** start application
```bash
python3 main.py 
```

## 🔍 Usage

### Process PDFs
- **Step 1:** add your PDFs to the data directory
- **Step 2:** launch application
```python
python3 main.py
```
- **Step 3:** select if your PDFs is structures by Markdowns (Chapters, Titles, ...) or not
- **Step 4:** Choose the chunk size aka the average sizes of your paragraph
- **Step 5:** Wait & enjoy chating with your data !

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazingFeature`)
3. Commit your changes (`git commit -am 'Add some amazingFeature'`)
4. Push to the branch (`git push origin feature/amazingFeature`)
5. Open a pull request

## 🏆 Credits

This is a solo project made by [myself](https://github.com/wayzeek)

## ⚖️ License

```
MIT License - see the [LICENSE](LICENSE) file for details
```
