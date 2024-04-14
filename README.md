# 🤖 CustomGPT - Chat with your Data 📚 

CustomGPT is a *sophisticated*, **multilingual chatbot** designed to streamline the *extraction, processing, and interaction* with text data from **PDF documents**.\
Leveraging *advanced NLP* and *machine learning models*, it enables *rich*, *interactive communication* across multiple languages, making it ideal for businesses, educational institutions or individuals dealing with diverse document formats.

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

CustomGPT harnesses the power of *conversational AI* to enhance the way organizations or individuals handle document-based information.\
By *automatically extracting* and *analyzing text from PDFs* and facilitating dynamic interactions through its chatbot interface, CustomGPT transforms static data into *actionable insights*. \
This integration of document processing with advanced dialogue systems offers a *unique solution* that significantly *boosts productivity* and *user engagement*.

### Screenshot
![image](https://github.com/wayzeek/CustomGPT/assets/112975047/a8cb0a07-af4a-4971-b8d6-002fac673271)


## ✨ Features

- **PDF Text Extraction**: Utilizes **PyPDF2** for efficient text extraction from PDFs, handling multiple layouts and formats.
- **Advanced Text Processing**: Integrates **tokenizers** and **Spacy** text splitters for text segmentation, and employs Spacy Language Detection module for robust language detection, ensuring precise text analysis.
- **Multilingual Support**: Powered by multiple instances of the transformer-based large language models **Mistral-7B-Instruct-v0.2**, supports interactions in multiple languages using **Hugging Face API**:
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
- **Step 3:** *select* if your PDFs is *structured* by Markdowns (Chapters, Titles, ...) *or not*
- **Step 4:** Choose the chunk size *aka* the average sizes of your paragraph
- **Step 5:** *Wait* & **enjoy chating with your data** !

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazingFeature`)
3. Commit your changes (`git commit -am 'Add some amazingFeature'`)
4. Push to the branch (`git push origin feature/amazingFeature`)
5. Open a pull request

## 🏆 Credits

This is a solo project made by [myself](https://github.com/wayzeek)

## ⚖️ License

MIT License - see the [LICENSE](LICENSE) file for details
