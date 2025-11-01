![mariadbimage](https://github.com/user-attachments/assets/763034b7-7ecb-4397-875d-0397b878e9ff)

# Native MariaDB Vector Store Support for MindSQL

## MariaDB Python Hackathon 2025 - Integration Track

### Important Links

- **Pull Request:** [#34 - Add MariaDB Integration with Native VECTOR Support](https://github.com/Mindinventory/MindSQL/pull/34)
- **Hackathon Platform:** [MariaDB Python Hackathon](https://mariadb-python.hackerearth.com/)
- **Demo Video:** [YouTube Demo](https://youtu.be/VIDEO_ID) _(To be added)_
- **Original Repository:** [MindSQL by Mindinventory](https://github.com/Mindinventory/MindSQL)

### Submission Checklist

- [x] **Code Repository:** Complete implementation with MariaDB native VECTOR(384) support
- [x] **Pull Request:** [PR #34](https://github.com/Mindinventory/MindSQL/pull/34) submitted to MindSQL repository
- [x] **Documentation:** Comprehensive README, API reference, usage examples
- [ ] **Demo Video:** 2-4 minute YouTube video showcasing the project
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

- **Database:** MariaDB 10.7+ (VECTOR support required)
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
- MariaDB 10.7+ with VECTOR support
- 4GB RAM minimum

### Quick Setup

```bash
# Clone repository
git clone https://github.com/Mindinventory/MindSQL.git
cd MindSQL

# Install dependencies
pip install -r requirements_demo.txt
pip install mariadb sentence-transformers google-generativeai

# Verify MariaDB VECTOR support
mysql -u root -p -e "SELECT VERSION();"  # Should be 10.7+
```

### Environment Configuration

Create `.env` file:
```env
API_KEY=your_google_gemini_api_key
LLM_MODEL=gemini-1.5-flash
DB_URL=mariadb://username:password@localhost:3306/database_name
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


### Interactive Demo CLI

```bash
cd tests
python mindsql_demo_cli.py
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

Thank you for organizing the MariaDB Python Hackathon 2024, developing native VECTOR data type support, and maintaining the MariaDB Python connector.

**Hackathon:** [MariaDB Python Hackathon 2024](https://mariadb-python.hackerearth.com/) - Integration Track

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

