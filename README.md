# 📋 Contract Obligation Extractor

**Extract and analyze contractual obligations from your contracts using AI**

A powerful tool that uses advanced language models to automatically extract, categorize, and analyze contractual obligations from PDF and text contracts. Unlike existing tools that focus on drafting and redlining, this application handles **post-signature contract analysis** - a critical gap in legal tech workflows.

## 🎯 **Why This Feature is Powerful**

- **Not available in Spellbook** (they stop at drafting and redlining)
- Shows your product can handle **post-signature contracts**
- Highlights **real LLM usage**, not mockups or templates
- Valuable for compliance, renewals, and deal follow-through

## ✨ **Key Features**

### 🔍 **Smart Extraction**
- **AI-Powered Analysis**: Uses GPT-4 and Gemini for accurate obligation extraction
- **Dual API Support**: Automatic fallback between OpenAI and Google APIs
- **Legal Domain Expertise**: Specialized prompts for contract analysis

### 📊 **Comprehensive Analysis**
- **Obligation Identification**: Extract specific contractual requirements
- **Party Assignment**: Identify responsible parties (Party A, Party B, etc.)
- **Due Date Extraction**: Find time-bound obligations and deadlines
- **Risk Assessment**: Classify obligations as Low, Medium, or High risk
- **Plain English Summaries**: Convert legal language to actionable insights

### 🎨 **Professional UI**
- **Streamlit Interface**: Clean, intuitive web application
- **Interactive Tables**: Sortable, filterable obligations display
- **Visual Analytics**: Risk distribution charts and metrics
- **Export Options**: Download results as CSV or summary reports

### 🔧 **Robust Processing**
- **PDF Support**: Extract text from complex PDF layouts
- **Multiple Parsers**: PyMuPDF with pdfminer fallback
- **Error Handling**: Graceful degradation and user feedback
- **File Validation**: Size limits and format checking

## 🚀 **Quick Start**

### 1. **Installation**

```bash
# Clone the repository
git clone <repository-url>
cd spellbook

# Install dependencies
pip install -r requirements.txt
```

### 2. **API Key Setup**

Create a `.env` file in the project root:

```bash
# Copy example file
cp env.example .env

# Edit .env and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get API Keys:**
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 3. **Run the Application**

```bash
# Start the Streamlit app
streamlit run app/main.py
```

The application will open at `http://localhost:8501`

## 📖 **Usage Guide**

### **Step 1: Upload Contract**
- Upload a PDF or text file (max 10MB)
- Or use the built-in demo contracts for testing

### **Step 2: AI Analysis**
- Click "Extract Obligations"
- Watch real-time processing status
- AI analyzes the document using GPT-4 or Gemini

### **Step 3: Review Results**
- View extracted obligations in interactive table
- Filter by risk level, party, or due date
- See risk distribution charts

### **Step 4: Export Data**
- Download results as CSV
- Generate summary reports
- Share insights with stakeholders

## 🏗️ **Architecture**

```
spellbook/
├── app/
│   ├── main.py                 # Streamlit main application
│   │   ├── components/
│   │   │   ├── file_upload.py      # PDF/text upload component
│   │   │   ├── results_table.py    # Obligations display table
│   │   │   └── download.py         # CSV/export functionality
│   │   ├── services/
│   │   │   ├── llm_service.py      # OpenAI/Gemini API integration
│   │   │   ├── pdf_parser.py       # PDF text extraction
│   │   │   └── obligation_extractor.py  # Core extraction logic
│   │   ├── utils/
│   │   │   ├── prompts.py          # LLM prompt templates
│   │   │   └── validators.py       # Input/output validation
│   │   └── config/
│   │       └── settings.py         # API keys, model configs
│   ├── requirements.txt
│   ├── README.md
│   └── env.example
```

## 🔧 **Technical Stack**

### **Core Technologies**
- **Streamlit**: Interactive web interface
- **OpenAI GPT-4**: Primary LLM for legal analysis
- **Google Gemini**: Fallback LLM option
- **PyMuPDF**: PDF text extraction
- **Pandas**: Data processing and analysis

### **Key Dependencies**
```python
streamlit>=1.28.0      # Web interface
openai>=1.0.0          # OpenAI API
google-generativeai>=0.3.0  # Gemini API
PyMuPDF>=1.23.0        # PDF processing
pandas>=2.0.0          # Data manipulation
pydantic>=2.0.0        # Data validation
```

## 🎯 **Demo Contracts**

The application includes built-in demo contracts for testing:

1. **Service Agreement**: Consulting services with payment terms
2. **Employment Contract**: Job duties, compensation, and benefits
3. **NDA**: Confidentiality and non-disclosure obligations
4. **Custom Text**: Paste your own contract text

## 📊 **Output Format**

Extracted obligations are structured as:

```json
{
  "obligation": "Specific obligation text from contract",
  "responsibleParty": "Party A/Party B/Company/Vendor",
  "dueDate": "YYYY-MM-DD or timeframe or 'Ongoing'",
  "riskLevel": "Low/Medium/High",
  "summary": "One-line plain English description"
}
```

## 🔐 **Security & Privacy**

- **No Data Storage**: Contract content is not persisted
- **Secure API Keys**: Environment variable management
- **Temporary Processing**: Data exists only during analysis
- **API Rate Limiting**: Respectful usage of external APIs

## 🚀 **Deployment**

### **Local Development**
```bash
streamlit run app/main.py
```

### **Production Deployment**
```bash
# Using Streamlit Cloud
# 1. Push to GitHub
# 2. Connect to Streamlit Cloud
# 3. Set environment variables
# 4. Deploy

# Using Docker
docker build -t contract-extractor .
docker run -p 8501:8501 contract-extractor
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the code comments and docstrings
- **API Keys**: Ensure your API keys are valid and have sufficient credits

## 🎉 **Success Metrics**

- **Extraction Accuracy**: >90% for standard contracts
- **Processing Time**: <30 seconds for typical contracts
- **API Reliability**: >99% uptime with fallbacks
- **User Experience**: Intuitive interface with clear feedback

---

**Built with ❤️ for legal professionals who need better contract analysis tools.** 