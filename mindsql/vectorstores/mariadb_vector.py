"""
MariaDB Vector Store Implementation

This module provides a vector store implementation using MariaDB's native VECTOR data type
and official MariaDB connector. It supports embedding storage, similarity search, and 
full-text search capabilities for AI/ML applications.
"""
import json
import os
import uuid
from typing import List
import mariadb
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from mindsql.vectorstores import IVectorstore


class MariaDBVectorStore(IVectorstore):
    """
    MariaDB Vector Store using native VECTOR data type.
    
    Provides vector storage and retrieval capabilities with MariaDB's
    native VECTOR data type, FULLTEXT search, and JSON support.
    """
    
    def __init__(self, config=None):
        """Initialize MariaDB Vector Store.
        
        Args:
            config (dict): Database connection parameters
                Required: host, user, password
                Optional: port (default 3306), database, collection_name
        """
        if config is None:
            raise ValueError("MariaDB configuration is required")
        
        # Separate collection_name from connection params
        self.collection_name = config.get('collection_name', 'mindsql_vectors')
        
        # Connection params only (no collection_name)
        self.connection_params = {
            'host': config.get('host', 'localhost'),
            'port': config.get('port', 3306),
            'user': config.get('user'),
            'password': config.get('password'),
        }
        
        # Add database if provided
        if 'database' in config and config['database']:
            self.connection_params['database'] = config['database']
        
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        
        self._init_database()
    
    def _init_database(self):
        """Initialize MariaDB vector storage tables."""
        try:
            conn = mariadb.connect(**self.connection_params)
            cursor = conn.cursor()
            
            cursor.execute(f"DROP TABLE IF EXISTS {self.collection_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {self.collection_name}_sql_pairs")
            
            cursor.execute(f"""
                CREATE TABLE {self.collection_name} (
                    id VARCHAR(36) PRIMARY KEY,
                    document TEXT NOT NULL,
                    embedding VECTOR({self.dimension}) NOT NULL,
                    metadata JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_created_at (created_at),
                    FULLTEXT(document)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            cursor.execute(f"""
                CREATE TABLE {self.collection_name}_sql_pairs (
                    id VARCHAR(36) PRIMARY KEY,
                    question TEXT NOT NULL,
                    sql_query TEXT NOT NULL,
                    embedding VECTOR({self.dimension}) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FULLTEXT(question, sql_query)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            error_msg = str(e)
            if 'caching_sha2_password' in error_msg or 'plugin' in error_msg.lower():
                raise RuntimeError(
                    f"MariaDB authentication plugin error. "
                    f"Run 'fix_mariadb_auth.bat' (Windows) or 'fix_mariadb_auth.sh' (Linux/Mac) to fix. "
                    f"Original error: {error_msg[:100]}"
                )
            raise RuntimeError(f"Failed to initialize MariaDB VECTOR Store: {e}")
    
    def _format_vector_for_insertion(self, embedding_array):
        """Format embedding array for VEC_FromText() function.
        
        Args:
            embedding_array (list): Embedding vector as list of floats
            
        Returns:
            str: JSON formatted string for VEC_FromText()
        """
        if len(embedding_array) != self.dimension:
            raise ValueError(f"Expected {self.dimension} dimensions, got {len(embedding_array)}")
        
        return '[' + ','.join(f'{float(x)}' for x in embedding_array) + ']'
    
    def add_ddl(self, ddl: str):
        """Add DDL to MariaDB vector store.
        
        Args:
            ddl (str): DDL statement to store
        """
        embedding = self.embedding_model.encode(ddl).tolist()
        vector_json = self._format_vector_for_insertion(embedding)
        
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        doc_id = str(uuid.uuid4())
        cursor.execute(f"""
            INSERT INTO {self.collection_name} 
            (id, document, embedding, metadata) 
            VALUES (?, ?, VEC_FromText(?), ?)
        """, (doc_id, ddl, vector_json, json.dumps({"type": "ddl"})))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def add_question_sql(self, question: str, sql: str):
        """Add question-SQL pair to vector store.
        
        Args:
            question (str): Natural language question
            sql (str): Corresponding SQL query
        """
        embedding = self.embedding_model.encode(question).tolist()
        vector_json = self._format_vector_for_insertion(embedding)
        
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        doc_id = str(uuid.uuid4())
        cursor.execute(f"""
            INSERT INTO {self.collection_name}_sql_pairs 
            (id, question, sql_query, embedding) 
            VALUES (?, ?, ?, VEC_FromText(?))
        """, (doc_id, question, sql, vector_json))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_similar_question_sql(self, question: str, n_results: int = 5):
        """Find similar questions using FULLTEXT search.
        
        Args:
            question (str): Question to find matches for
            n_results (int): Maximum number of results
            
        Returns:
            list: List of similar question-SQL pairs
        """
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT question, sql_query,
                   MATCH(question, sql_query) AGAINST (? IN NATURAL LANGUAGE MODE) as text_score
            FROM {self.collection_name}_sql_pairs 
            WHERE MATCH(question, sql_query) AGAINST (? IN NATURAL LANGUAGE MODE)
            ORDER BY text_score DESC 
            LIMIT ?
        """, (question, question, n_results))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        similar_pairs = []
        for row in results:
            similar_pairs.append({
                'question': row[0],
                'sql': row[1],
                'similarity': row[2],
                'text_score': row[2]
            })
        
        return similar_pairs
    
    def retrieve_relevant_ddl(self, question: str, **kwargs) -> list:
        """Retrieve relevant DDL statements.
        
        Args:
            question (str): Question context (unused in current implementation)
            **kwargs: Additional parameters including n_results
            
        Returns:
            list: List of DDL statements
        """
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT document
            FROM {self.collection_name} 
            WHERE JSON_EXTRACT(metadata, '$.type') = 'ddl'
            ORDER BY created_at DESC
            LIMIT ?
        """, (kwargs.get('n_results', 5),))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [row[0] for row in results]
    
    def retrieve_relevant_documentation(self, question: str, **kwargs) -> list:
        """Retrieve relevant documentation.
        
        Args:
            question (str): Question context (unused in current implementation)
            **kwargs: Additional parameters including n_results
            
        Returns:
            list: List of documentation strings
        """
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT document
            FROM {self.collection_name} 
            WHERE JSON_EXTRACT(metadata, '$.type') = 'documentation'
            ORDER BY created_at DESC
            LIMIT ?
        """, (kwargs.get('n_results', 5),))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [row[0] for row in results]
    
    def retrieve_relevant_question_sql(self, question: str, **kwargs) -> list:
        """Retrieve relevant question-SQL pairs"""
        n_results = kwargs.get('n_results', 3)
        return self.get_similar_question_sql(question, n_results)
    
    def index_question_sql(self, question: str, sql: str, **kwargs) -> str:
        """Add a question-SQL pair to the vectorstore.
        
        Args:
            question (str): Natural language question
            sql (str): Corresponding SQL query
            **kwargs: Additional parameters (unused)
            
        Returns:
            str: Success or error message
        """
        try:
            self.add_question_sql(question, sql)
            return "Successfully added question-SQL pair to MariaDB VECTOR store"
        except Exception as e:
            return f"Failed to add question-SQL pair: {e}"
    
    def index_ddl(self, ddl: str, **kwargs) -> str:
        """Add DDL to the vectorstore.
        
        Args:
            ddl (str): DDL statement
            **kwargs: Additional parameters (unused)
            
        Returns:
            str: Success or error message
        """
        try:
            self.add_ddl(ddl)
            return "Successfully added DDL to MariaDB VECTOR store"
        except Exception as e:
            return f"Failed to add DDL: {e}"
    
    def index_documentation(self, documentation: str, **kwargs) -> str:
        """Add documentation to the vectorstore.
        
        Args:
            documentation (str): Documentation text
            **kwargs: Additional parameters (unused)
            
        Returns:
            str: Success or error message
        """
        try:
            embedding = self.embedding_model.encode(documentation).tolist()
            vector_json = self._format_vector_for_insertion(embedding)
            
            conn = mariadb.connect(**self.connection_params)
            cursor = conn.cursor()
            
            doc_id = str(uuid.uuid4())
            cursor.execute(f"""
                INSERT INTO {self.collection_name} 
                (id, document, embedding, metadata) 
                VALUES (?, ?, VEC_FromText(?), ?)
            """, (doc_id, documentation, vector_json, json.dumps({"type": "documentation"})))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return "Successfully added documentation to MariaDB VECTOR store"
        except Exception as e:
            return f"Failed to add documentation: {e}"
    
    def fetch_all_vectorstore_data(self, **kwargs) -> pd.DataFrame:
        """Fetch all data from the vectorstore.
        
        Args:
            **kwargs: Additional parameters (unused)
            
        Returns:
            pd.DataFrame: Combined data from all vector store tables
        """
        conn = mariadb.connect(**self.connection_params)
        
        main_df = pd.read_sql(f"SELECT id, document, created_at FROM {self.collection_name}", conn)
        sql_pairs_df = pd.read_sql(f"SELECT id, question, sql_query, created_at FROM {self.collection_name}_sql_pairs", conn)
        
        conn.close()
        
        combined_data = []
        
        for _, row in main_df.iterrows():
            combined_data.append({
                'id': row['id'],
                'content': row['document'],
                'type': 'document',
                'created_at': row['created_at']
            })
        
        for _, row in sql_pairs_df.iterrows():
            combined_data.append({
                'id': row['id'],
                'content': f"Q: {row['question']} | SQL: {row['sql_query']}",
                'type': 'question_sql',
                'created_at': row['created_at']
            })
        
        return pd.DataFrame(combined_data)
    
    def delete_vectorstore_data(self, item_id: str, **kwargs) -> bool:
        """Delete data from the vectorstore.
        
        Args:
            item_id (str): ID of item to delete
            **kwargs: Additional parameters (unused)
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        conn = mariadb.connect(**self.connection_params)
        cursor = conn.cursor()
        
        cursor.execute(f"DELETE FROM {self.collection_name} WHERE id = ?", (item_id,))
        main_deleted = cursor.rowcount
        
        cursor.execute(f"DELETE FROM {self.collection_name}_sql_pairs WHERE id = ?", (item_id,))
        pairs_deleted = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return (main_deleted + pairs_deleted) > 0
    
    def add_documents(self, documents: List[str]):
        """Add multiple documents to MariaDB vector store.
        
        Args:
            documents (List[str]): List of documents to add
        """
        for doc in documents:
            self.add_ddl(doc)