# Virtual Risk Project Manager

A Streamlit app to generate a comprehensive risk assessment template based on user inputs and selected frameworks/regulations.

## Setup

### Prerequisites
- Python 3.7+
- Streamlit
- OpenAI API key
- PyMuPDF

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/virtual-risk-project-manager.git
   cd virtual-risk-project-manager
Create a virtual environment and activate it:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:

sh
Copy code
pip install -r requirements.txt
Create a .env file in the root directory and add your OpenAI API key:

plaintext
Copy code
OPENAI_API_KEY=your-openai-api-key
Running the App
Run the Streamlit app:

sh
Copy code
streamlit run app.py
Open your browser and navigate to http://localhost:8501 to access the app.

Usage
Follow the instructions on the app interface to generate a comprehensive risk assessment template.

Features
Input business, project, and tool profiles
Add extra comments about bespoke risk processes
Select relevant frameworks/regulations (GDPR, NIST, ISO)
Upload standards and regulations as PDFs
Generate and download a risk template in CSV format
Edit the generated template with additional comments
Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License.
