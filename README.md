![mariadbimage](https://github.com/user-attachments/assets/763034b7-7ecb-4397-875d-0397b878e9ff)

# Native MariaDB Vector Store Support for MindSQL

## MariaDB Python Hackathon 2025 - Integration Track

### Important Links

- **Pull Request:** [#34 - Add MariaDB Integration with Native VECTOR Support](https://github.com/Mindinventory/MindSQL/pull/34)
- **Hackathon Platform:** [MariaDB Python Hackathon](https://mariadb-python.hackerearth.com/)
- **Demo Video:** [YouTube Demo](https://www.youtube.com/watch?v=Q67DPPTeAkQ)
- **Original Repository:** [MindSQL by Mindinventory](https://github.com/Mindinventory/MindSQL)

### Submission Checklist

- [x] **Code Repository:** Complete implementation with MariaDB native VECTOR(384) support
- [x] **Pull Request:** [PR #34](https://github.com/Mindinventory/MindSQL/pull/34) submitted to MindSQL repository
- [x] **Documentation:** Comprehensive README, API reference, usage examples
- [x] **Demo Video:** 2-4 minute YouTube video showcasing the project
- [x] **LinkedIn Post:** Announced submission on LinkedIn

---

## Overview

<img width="1920" height="544" alt="Gemini_Generated_Image_d93qe1d93qe1d93q" src="https://github.com/user-attachments/assets/a839758d-a47e-405a-ad92-821cfef84198" />

This project integrates MariaDB's native VECTOR(384) data type with MindSQL, a Python RAG framework for text-to-SQL conversion. Production-ready vector store implementation that enables unified vector-relational storage, eliminating the need for separate vector database infrastructure alongside production MariaDB instances.

### Key Benefits

- **Unified Infrastructure:** Single MariaDB instance for relational data and vector embeddings
- **Native Performance:** Leverages MariaDB's VECTOR(384) data type with ACID guarantees
- **Hybrid Search:** Combines FULLTEXT indexing with vector similarity
- **Query Learning:** Persistent memory system that improves accuracy over time
- **Production Ready:** Comprehensive error handling, connection management, full testing

---

## Problem & Solution

### The Problem

Organizations using MindSQL with MariaDB face infrastructure fragmentation - separate vector databases (ChromaDB, FAISS) required alongside MariaDB, increasing operational complexity, costs, and network latency.

### Our Solution

Native MariaDB Vector Store implementing MindSQL's IVectorstore interface with three core capabilities:

1. **Semantic Schema Intelligence:** Automatically vectorizes DDL schemas using VECTOR(384) columns
2. **AI-Powered Query Learning:** Stores successful question-SQL pairs for continuous improvement
3. **Intelligent Query Optimization:** Combines FULLTEXT search with vector similarity for optimal context retrieval

### Technology Stack

- **Database:** MariaDB 11.7+ (VECTOR support required)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Connector:** Official mariadb Python package
- **Framework:** MindSQL RAG Core
- **LLM Support:** Google Gemini, OpenAI, Ollama, Llama

---

## Architecture

<img width="918" height="604" alt="Screenshot 2025-10-11 000201" src="https://github.com/user-attachments/assets/9167d6a4-41fd-4438-8805-123d2afe4158" />


### Database Schema

**Main Collection (mindsql_vectors):**
```sql
CREATE TABLE mindsql_vectors (
    id VARCHAR(36) PRIMARY KEY,
    document TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    FULLTEXT(document)
) ENGINE=InnoDB;
```

**Query Memory (mindsql_vectors_sql_pairs):**
```sql
CREATE TABLE mindsql_vectors_sql_pairs (
    id VARCHAR(36) PRIMARY KEY,
    question TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT(question, sql_query)
) ENGINE=InnoDB;
```

### RAG Pipeline

1. **Embedding:** User query → 384-dimensional vector
2. **Retrieval:** FULLTEXT + vector similarity → relevant DDLs and examples
3. **Augmentation:** Context enriches LLM prompt
4. **Generation:** LLM generates SQL with context
5. **Learning:** Successful pairs stored for future use

---

## Installation

### Prerequisites

- Python 3.11+
- MariaDB 11.7+ with VECTOR support
- 4GB RAM minimum

## Installation & Setup

### Step 1: Install MariaDB

**Windows:**
```bash
choco install mariadb
```
Or download from [MariaDB Downloads](https://mariadb.org/download/)

**Linux:**
```bash
sudo apt update
sudo apt install mariadb-server mariadb-client
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

**macOS:**
```bash
brew install mariadb
brew services start mariadb
```

Verify installation:
```bash
mariadb --version
```
Version must be 10.7 or higher for VECTOR support.

### Step 2: Setup MariaDB Database

```bash
mariadb -u root -p
```

Create database and user:
```sql
CREATE DATABASE mindsql_demo;
CREATE USER 'mindsql_user'@'localhost' IDENTIFIED BY 'mindsql_password';
GRANT ALL PRIVILEGES ON mindsql_demo.* TO 'mindsql_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Clone and Install Python Dependencies

```bash
git clone https://github.com/Mindinventory/MindSQL.git
cd MindSQL
```

Install Python packages:
```bash
pip install mariadb
pip install sentence-transformers
pip install google-generativeai
pip install rich
pip install python-dotenv
pip install pandas
pip install numpy
```

Or install all at once:
```bash
pip install -r requirements_demo.txt
```

### Step 4: Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### Step 5: Configure Environment

Create `.env` file in project root:
```env
API_KEY=your_google_gemini_api_key_here
LLM_MODEL=gemini-1.5-flash
DB_URL=mariadb://mindsql_user:mindsql_password@localhost:3306/mindsql_demo
```

### Step 6: Add Sample Data

```bash
mariadb -u mindsql_user -p mindsql_demo
```

Create sample tables:
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers (name, email, city) VALUES
('John Doe', 'john@email.com', 'New York'),
('Jane Smith', 'jane@email.com', 'Los Angeles'),
('Bob Johnson', 'bob@email.com', 'Chicago');

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-10-15', 150.00, 'completed'),
(2, '2024-10-20', 200.00, 'completed'),
(1, '2024-10-25', 75.00, 'pending');

EXIT;
```

### Step 7: Run Demo CLI

```bash
cd tests
python mindsql_demo_cli.py
```

The demo will:
1. Connect to MariaDB
2. Discover your tables automatically
3. Index table schemas into vector store
4. Let you ask questions in natural language

### Step 8: Try Sample Queries

Once demo is running, try these questions:
```
Show all customers
Which customers are from New York?
What are the total orders for each customer?
Show pending orders
```

---

## Usage

### Basic Example

```python
from mindsql.core import MindSQLCore
from mindsql.databases import MariaDB
from mindsql.vectorstores import MariaDBVectorStore
from mindsql.llms import GoogleGenAi

# Configure components
vector_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'collection_name': 'mindsql_vectors'
}

llm_config = {
    'api_key': 'your_api_key',
    'model': 'gemini-1.5-flash'
}

# Initialize MindSQL with MariaDB Vector Store
minds = MindSQLCore(
    database=MariaDB(),
    vectorstore=MariaDBVectorStore(config=vector_config),
    llm=GoogleGenAi(config=llm_config)
)

# Create connection and index schemas
connection = minds.database.create_connection(
    url="mariadb://user:pass@localhost:3306/mydb"
)
minds.index_all_ddls(connection=connection, db_name='mydb')

# Natural language to SQL
response = minds.ask_db(
    question="Find customers who haven't ordered in 3 months",
    connection=connection
)

print(response['sql'])
print(response['result'])
connection.close()
```

## API Reference

### MariaDBVectorStore Class

```python
class MariaDBVectorStore(IVectorstore):
    """MariaDB Vector Store implementation."""
    
    def __init__(self, config: dict):
        """Initialize with connection parameters.
        
        Args:
            config: Dict with host, port, user, password, database, collection_name
        """
    
    def index_ddl(self, ddl: str, **kwargs) -> str:
        """Index a DDL statement. Returns success/error message."""
    
    def index_question_sql(self, question: str, sql: str, **kwargs) -> str:
        """Index question-SQL pair for learning."""
    
    def retrieve_relevant_ddl(self, question: str, **kwargs) -> list:
        """Retrieve relevant DDL statements."""
    
    def retrieve_relevant_question_sql(self, question: str, **kwargs) -> list:
        """Retrieve similar question-SQL pairs with scores."""
    
    def index_documentation(self, documentation: str, **kwargs) -> str:
        """Index documentation text."""
    
    def fetch_all_vectorstore_data(self, **kwargs) -> pd.DataFrame:
        """Fetch all stored data as DataFrame."""
    
    def delete_vectorstore_data(self, item_id: str, **kwargs) -> bool:
        """Delete specific entry. Returns success boolean."""
```
---

## Contributing

We welcome contributions! This integration was created for MariaDB Python Hackathon 2025.

### Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/MindSQL.git
cd MindSQL
git checkout -b feature/your-feature

python -m venv venv
source venv/bin/activate
pip install -r requirements_demo.txt
pip install pytest black flake8

# Make changes and test
pytest tests/ -v
black mindsql/ tests/
flake8 mindsql/ tests/

git commit -m "feat: your feature"
git push origin feature/your-feature
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Reporting Issues

**Bug Reports:** Description, reproduction steps, environment details, error messages

**Feature Requests:** Clear description, use case, proposed solution

---

## Acknowledgments

### MariaDB Foundation

Thank you for organizing the MariaDB Python Hackathon 2025, developing native VECTOR data type support, and maintaining the MariaDB Python connector.

**Hackathon:** [MariaDB Python Hackathon 2025](https://mariadb-python.hackerearth.com/) - Integration Track

### MindSQL Project

Thank you to the MindSQL maintainers for creating an excellent RAG framework with clean, extensible architecture.

**Repository:** [https://github.com/Mindinventory/MindSQL](https://github.com/Mindinventory/MindSQL)

### Open Source Community

Built upon outstanding work from sentence-transformers, MariaDB Server, and the Python ecosystem.

---

## Resources

### Documentation

- [MariaDB VECTOR Data Type](https://mariadb.com/kb/en/vector-data-type/)
- [MariaDB Python Connector](https://mariadb.com/docs/appdev/connector-python/)
- [MindSQL Documentation](https://github.com/Mindinventory/MindSQL)
- [sentence-transformers](https://www.sbert.net/)

### Support

- **GitHub Issues:** [MindSQL Issues](https://github.com/Mindinventory/MindSQL/issues)
- **Security:** See [SECURITY.md](SECURITY.md) for vulnerability reporting

---

### Team

**Team Name:** Squirtle Squad  
**Track:** Integration  
**Project:** Native MariaDB Vector Store for MindSQL RAG Framework

