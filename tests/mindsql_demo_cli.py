#!/usr/bin/env python3
"""
MindSQL Interactive CLI - Professional Demo
============================================
Beautiful, flexible CLI for MindSQL + MariaDB integration
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Force UTF-8 on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.tree import Tree
    from rich import box
    from rich.live import Live
    from rich.align import Align
    from rich.columns import Columns
    from rich.syntax import Syntax
except ImportError:
    print("Installing required package: rich")
    os.system(f"{sys.executable} -m pip install rich -q")
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.tree import Tree
    from rich import box
    from rich.syntax import Syntax

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

console = Console()


class MindSQLCLI:
    """Professional MindSQL CLI"""
    
    def __init__(self):
        self.console = console
        self.config = {}
        self.database = None
        self.vectorstore = None
        self.llm = None
        self.mindsql = None
        self.connection = None
        self.database_name = None
        self.tables = []
        
    def show_banner(self):
        """Futuristic cyber-style banner with colors and animations"""
        from rich.style import Style
        import time
        
        # Clear and show loading animation
        self.console.clear()
        
        # Cyberpunk-style banner with gradient colors
        title = Text()
        title.append("\n\n")
        title.append("███╗   ███╗██╗███╗   ██╗██████╗ ███████╗ ██████╗ ██╗     \n", style=Style(color="bright_cyan", bold=True))
        title.append("████╗ ████║██║████╗  ██║██╔══██╗██╔════╝██╔═══██╗██║     \n", style=Style(color="cyan", bold=True))
        title.append("██╔████╔██║██║██╔██╗ ██║██║  ██║███████╗██║   ██║██║     \n", style=Style(color="blue", bold=True))
        title.append("██║╚██╔╝██║██║██║╚██╗██║██║  ██║╚════██║██║▄▄ ██║██║     \n", style=Style(color="magenta", bold=True))
        title.append("██║ ╚═╝ ██║██║██║ ╚████║██████╔╝███████║╚██████╔╝███████╗\n", style=Style(color="bright_magenta", bold=True))
        title.append("╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚══▀▀═╝ ╚══════╝\n", style=Style(color="bright_magenta", bold=True))
        title.append("\n")
        
        self.console.print(Align.center(title))
        time.sleep(0.2)
        
        # Subtitle with shapes
        subtitle = Text()
        subtitle.append("▶ ", style=Style(color="yellow", bold=True))
        subtitle.append("RAG-Powered Text-to-SQL Framework", style=Style(color="bright_white", bold=True))
        subtitle.append(" ◀\n", style=Style(color="yellow", bold=True))
        self.console.print(Align.center(subtitle))
        time.sleep(0.2)
        
        # Feature highlights with shape icons
        features = Text()
        features.append("\n")
        features.append("    ● ", style=Style(color="bright_cyan", bold=True))
        features.append("Natural Language to SQL  ", style=Style(color="white"))
        features.append("■ ", style=Style(color="bright_green", bold=True))
        features.append("Vector-Enhanced Retrieval  ", style=Style(color="white"))
        features.append("▲ ", style=Style(color="bright_magenta", bold=True))
        features.append("Multi-Database Support\n", style=Style(color="white"))
        features.append("\n")
        self.console.print(Align.center(features))
        time.sleep(0.2)
        
        # Separator
        separator = Text("─" * 80 + "\n", style=Style(color="bright_cyan", dim=True))
        self.console.print(Align.center(separator))
        time.sleep(0.1)
        
        # System information panel
        self.console.print()
        self.console.print("[bold bright_magenta]▶ SYSTEM CAPABILITIES[/bold bright_magenta]\n")
        
        capabilities = [
            ("●", "bright_cyan", "Semantic Search", "Intelligent DDL retrieval using sentence transformers"),
            ("■", "bright_green", "RAG Pipeline", "Context-aware SQL generation with vector databases"),
            ("▲", "bright_yellow", "Multi-Engine", "MariaDB, MySQL, PostgreSQL, SQLite support"),
            ("◆", "bright_magenta", "LLM Integration", "Google Gemini, OpenAI, Ollama, and more"),
        ]
        
        for shape, color, title, desc in capabilities:
            self.console.print(f"  [bold {color}]{shape}[/bold {color}] [bold white]{title:20}[/bold white] [dim]{desc}[/dim]")
            time.sleep(0.15)
        
        self.console.print()
        self.console.print("[dim]Version 1.0.0  •  MariaDB Integration Ready  •  Powered by RAG Architecture[/dim]")
        self.console.print()
        
        # Loading animation
        with Progress(
            SpinnerColumn(style="bright_cyan"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("[bright_cyan]Initializing system components...", total=None)
            time.sleep(0.8)
        
        self.console.print("[bold bright_green]✓ System Ready[/bold bright_green]\n")
        time.sleep(0.3)
        
    def setup_configuration(self) -> Dict[str, Any]:
        """Interactive configuration setup with progress animation"""
        import time
        
        self.console.print()
        self.console.print("[bold bright_cyan]▼ SYSTEM INITIALIZATION[/bold bright_cyan]")
        self.console.print("[dim]Configuring MindSQL environment...[/dim]\n")
        
        # Try to load from .env
        api_key = os.getenv('API_KEY', '')
        db_url = os.getenv('DB_URL', '')
        llm_model = os.getenv('LLM_MODEL', 'gemini-1.5-flash')
        
        # Ask if user wants to use .env or manual input
        if api_key or db_url:
            use_env = Confirm.ask(
                "[cyan]● Found existing configuration  Use it?[/cyan]",
                default=True
            )
        else:
            use_env = False
            self.console.print("[yellow]▲ No configuration found  Manual setup required[/yellow]\n")
        
        if not use_env or not api_key:
            self.console.print("[bold cyan]■ LLM Configuration[/bold cyan]")
            api_key = Prompt.ask(
                "  Enter your API Key (Google Gemini)",
                password=True
            )
            
            llm_model = Prompt.ask(
                "  Enter LLM model name",
                default="gemini-1.5-flash"
            )
        
        if not use_env or not db_url:
            self.console.print("\n[bold cyan]■ Database Configuration[/bold cyan]")
            self.console.print("  [dim]Examples:[/dim]")
            self.console.print("  [dim]  MariaDB: mariadb://user:pass@localhost:3306/dbname[/dim]")
            self.console.print("  [dim]  MySQL:   mysql://user:pass@localhost:3306/dbname[/dim]")
            
            db_url = Prompt.ask("\n  Enter database URL")
        
        # Display configuration with progress animation
        self.console.print("\n")
        self.console.print("[bold bright_yellow]▶ Validating Configuration[/bold bright_yellow]")
        
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task1 = progress.add_task("[cyan]Checking API credentials...", total=None)
            time.sleep(0.5)
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("[cyan]Parsing database URL...", total=None)
            time.sleep(0.4)
            progress.update(task2, completed=True)
            
            task3 = progress.add_task("[cyan]Loading model configuration...", total=None)
            time.sleep(0.3)
            progress.update(task3, completed=True)
        
        # Display validated configuration
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        parsed = urlparse(db_url)
        safe_url = f"{parsed.scheme}://{parsed.username}:***@{parsed.hostname}:{parsed.port or 3306}/{parsed.path.lstrip('/')}"
        
        self.console.print()
        self.console.print("[bold bright_green]✓ Configuration Validated[/bold bright_green]\n")
        self.console.print(f"  [bold magenta]●[/bold magenta] [dim]API Key    [/dim] [bright_white]{masked_key}[/bright_white]")
        self.console.print(f"  [bold cyan]■[/bold cyan] [dim]Database   [/dim] [bright_white]{safe_url}[/bright_white]")
        self.console.print(f"  [bold yellow]▲[/bold yellow] [dim]LLM Model  [/dim] [bright_white]{llm_model}[/bright_white]")
        
        confirm = Confirm.ask("\n[yellow]▶ Proceed with this configuration?[/yellow]", default=True)
        if not confirm:
            self.console.print("[red]✗ Configuration cancelled[/red]")
            sys.exit(0)
        
        return {
            'api_key': api_key,
            'db_url': db_url,
            'llm_model': llm_model,
            'llm_temperature': 0.1
        }
    
    def select_database(self):
        """Select database type with futuristic design"""
        from mindsql.databases import MariaDB, MySql, Sqlite, Postgres
        import time
        
        self.console.print()
        self.console.print("[bold bright_cyan]▼ DATABASE ENGINE SELECTION[/bold bright_cyan]")
        self.console.print("[dim]Choose your database backend[/dim]\n")
        
        # Display options with shape icons
        options = [
            ("1", "●", "MariaDB", "Native VECTOR(384) support", "bright_magenta"),
            ("2", "■", "MySQL", "MySQL database", "bright_green"),
            ("3", "▲", "SQLite", "Lightweight file-based database", "bright_yellow"),
            ("4", "◆", "PostgreSQL", "Advanced SQL features", "bright_cyan"),
        ]
        
        for num, shape, name, desc, color in options:
            self.console.print(f"  [bold white]{num}[/bold white]  [bold {color}]{shape}[/bold {color}]  [bold white]{name:15}[/bold white] [dim]{desc}[/dim]")
        
        # Auto-detect from URL
        suggested = "1"
        if 'mysql://' in self.config['db_url']:
            suggested = "2"
        elif 'sqlite' in self.config['db_url']:
            suggested = "3"
        elif 'postgres' in self.config['db_url']:
            suggested = "4"
        
        choice = Prompt.ask(
            "\n[yellow]▶ Select database[/yellow] [dim][1/2/3/4][/dim]",
            choices=["1", "2", "3", "4"],
            default=suggested
        )
        
        db_map = {
            "1": ("MariaDB", MariaDB(), "●", "bright_magenta"),
            "2": ("MySQL", MySql(), "■", "bright_green"),
            "3": ("SQLite", Sqlite(), "▲", "bright_yellow"),
            "4": ("PostgreSQL", Postgres(), "◆", "bright_cyan"),
        }
        
        name, self.database, shape, color = db_map[choice]
        
        # Animated selection confirmation
        with Progress(
            SpinnerColumn(style=color),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(f"[{color}]Loading {name} engine...", total=None)
            time.sleep(0.6)
        
        self.console.print(f"\n[bold {color}]{shape} {name} Engine Selected[/bold {color}]\n")
        
    def select_vector_store(self):
        """Select vector store with futuristic design"""
        from mindsql.vectorstores import ChromaDB, Faiss
        import time
        
        try:
            from mindsql.vectorstores import MariaDBVectorStore
            has_mariadb = True
        except:
            has_mariadb = False
        
        self.console.print()
        self.console.print("[bold bright_cyan]▼ VECTOR STORE INITIALIZATION[/bold bright_cyan]")
        self.console.print("[dim]Configure your vector database[/dim]\n")
        
        # Display options with shape icons
        options = []
        if has_mariadb:
            options.append(("1", "●", "MariaDB Vector", "Native VECTOR(384) + FULLTEXT", "bright_magenta"))
        options.append(("2", "■", "ChromaDB", "Popular vector database", "bright_green"))
        options.append(("3", "▲", "FAISS", "Facebook AI Similarity Search", "bright_cyan"))
        
        for num, shape, name, desc, color in options:
            self.console.print(f"  [bold white]{num}[/bold white]  [bold {color}]{shape}[/bold {color}]  [bold white]{name:20}[/bold white] [dim]{desc}[/dim]")
        
        choices = ["2", "3"]
        if has_mariadb:
            choices.insert(0, "1")
        
        choice = Prompt.ask(
            "\n[yellow]▶ Select vector store[/yellow] [dim][{choices}][/dim]".replace("{choices}", "/".join(choices)),
            choices=choices,
            default="2"
        )
        
        if choice == "1" and has_mariadb:
            self.console.print()
            parsed = urlparse(self.config['db_url'])
            # MariaDB Vector Store config (don't pass collection_name to connection)
            vs_config = {
                'host': parsed.hostname,
                'port': parsed.port or 3306,
                'user': parsed.username,
                'password': parsed.password,
                'database': parsed.path.lstrip('/') or 'mindsql_vectors',
                'collection_name': 'mindsql_vectors'  # This is used by MariaDBVectorStore, not mariadb.connect()
            }
            try:
                with Progress(
                    SpinnerColumn(style="bright_magenta"),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                    transient=False
                ) as progress:
                    task1 = progress.add_task("[bright_magenta]Loading embedding model: sentence-transformers/all-MiniLM-L6-v2", total=None)
                    time.sleep(0.3)
                    progress.update(task1, description="[bright_magenta]● Embedding dimensions: 384")
                    time.sleep(0.2)
                    progress.update(task1, description="[bright_magenta]● Using device: cpu")
                    time.sleep(0.2)
                    progress.update(task1, description="[bright_magenta]● Collection: mindsql_vectors")
                    time.sleep(0.2)
                    progress.update(task1, description="[bright_magenta]● Initializing MariaDB Vector Store...")
                    
                    self.vectorstore = MariaDBVectorStore(config=vs_config)
                    name = "MariaDB Vector Store"
                    
                    progress.update(task1, description="[bright_magenta]● Created tables with native VECTOR(384) data type")
                    time.sleep(0.3)
                
                self.console.print(f"[bold bright_magenta]● MariaDB Vector Store Initialized[/bold bright_magenta]")
                self.console.print("[dim]  Hybrid vector-relational storage active[/dim]")
            except Exception as e:
                self.console.print(f"\n[yellow]▲ MariaDB Vector Store failed[/yellow] {str(e)[:150]}")
                self.console.print("[dim]  Note: Requires MariaDB 10.7+ with VECTOR support[/dim]")
                self.console.print("[bright_cyan]  Falling back to ChromaDB...[/bright_cyan]\n")
                
                with Progress(
                    SpinnerColumn(style="bright_green"),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                    transient=False
                ) as progress:
                    task = progress.add_task("[bright_green]■ Initializing ChromaDB...", total=None)
                    time.sleep(0.3)
                    self.vectorstore = ChromaDB()
                    name = "ChromaDB"
                
                self.console.print(f"[bold bright_green]■ ChromaDB Initialized[/bold bright_green]")
        elif choice == "2":
            self.console.print()
            with Progress(
                SpinnerColumn(style="bright_green"),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=False
            ) as progress:
                task = progress.add_task("[bright_green]Loading embedding model: sentence-transformers/all-MiniLM-L6-v2", total=None)
                time.sleep(0.3)
                progress.update(task, description="[bright_green]■ Embedding dimensions: 384")
                time.sleep(0.2)
                progress.update(task, description="[bright_green]■ Using device: cpu")
                time.sleep(0.2)
                progress.update(task, description="[bright_green]■ Storage path: ./chroma_db")
                time.sleep(0.2)
                progress.update(task, description="[bright_green]■ Initializing ChromaDB...")
                self.vectorstore = ChromaDB()
                name = "ChromaDB"
                time.sleep(0.2)
            
            self.console.print(f"[bold bright_green]■ ChromaDB Initialized[/bold bright_green]")
        else:
            self.console.print()
            with Progress(
                SpinnerColumn(style="bright_cyan"),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=False
            ) as progress:
                task = progress.add_task("[bright_cyan]Loading embedding model: sentence-transformers/all-MiniLM-L6-v2", total=None)
                time.sleep(0.3)
                progress.update(task, description="[bright_cyan]▲ Embedding dimensions: 384")
                time.sleep(0.2)
                progress.update(task, description="[bright_cyan]▲ Using device: cpu")
                time.sleep(0.2)
                progress.update(task, description="[bright_cyan]▲ Index path: ./faiss_index")
                time.sleep(0.2)
                progress.update(task, description="[bright_cyan]▲ Initializing FAISS...")
                self.vectorstore = Faiss()
                name = "FAISS"
                time.sleep(0.2)
            
            self.console.print(f"[bold bright_cyan]▲ FAISS Initialized[/bold bright_cyan]")
        
        self.console.print()
    
    def setup_llm(self):
        """Initialize LLM with futuristic design"""
        from mindsql.llms import GoogleGenAi
        
        self.console.print()
        self.console.print("[bold bright_cyan]▼ LLM INITIALIZATION[/bold bright_cyan]")
        self.console.print("[dim]Connecting to AI model...[/dim]\n")
        
        llm_config = {
            'api_key': self.config['api_key'],
            'model': self.config['llm_model']
        }
        
        with Progress(
            SpinnerColumn(style="bright_yellow"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=False
        ) as progress:
            task = progress.add_task("[bright_yellow]Connecting to Google Gemini API...", total=None)
            time.sleep(0.3)
            progress.update(task, description=f"[bright_yellow]◆ Model: {self.config['llm_model']}")
            time.sleep(0.2)
            progress.update(task, description=f"[bright_yellow]◆ Temperature: {self.config.get('temperature', 0.0)}")
            time.sleep(0.2)
            progress.update(task, description="[bright_yellow]◆ Provider: Google GenerativeAI")
            time.sleep(0.2)
            self.llm = GoogleGenAi(config=llm_config)
            time.sleep(0.2)
        
        self.console.print(f"[bold bright_yellow]◆ LLM Ready[/bold bright_yellow]")
        
        # Show complete stack configuration
        self.console.print()
        self.console.print("[bold bright_cyan]▶ STACK CONFIGURATION[/bold bright_cyan]\n")
        self.console.print(f"  [bold magenta]●[/bold magenta] [dim]Database     [/dim] [bright_white]{self.database.__class__.__name__}[/bright_white]")
        self.console.print(f"  [bold green]■[/bold green] [dim]Vector Store [/dim] [bright_white]{self.vectorstore.__class__.__name__}[/bright_white]")
        self.console.print(f"  [bold yellow]◆[/bold yellow] [dim]LLM Model    [/dim] [bright_white]{self.config['llm_model']}[/bright_white]")
        self.console.print()
    
    def connect_to_database(self):
        """Connect to database with futuristic design"""
        self.console.print()
        self.console.print("[bold bright_cyan]▼ DATABASE CONNECTION[/bold bright_cyan]")
        self.console.print("[dim]Establishing connection...[/dim]\n")
        
        with Progress(
            SpinnerColumn(style="bright_green"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=False
        ) as progress:
            task = progress.add_task("[bright_green]Connecting to database...", total=None)
            time.sleep(0.3)
            
            try:
                # Try MariaDB connector first
                self.connection = self.database.create_connection(self.config['db_url'])
                
                # If MariaDB connector fails, try MySQL fallback
                if self.connection is None and 'mariadb://' in self.config['db_url']:
                    progress.console.print("\n[yellow]▲ MariaDB connector failed[/yellow]")
                    progress.console.print("[dim]  Authentication plugin compatibility issue[/dim]")
                    progress.console.print("[bright_cyan]  Trying MySQL connector fallback...[/bright_cyan]\n")
                    from mindsql.databases import MySql
                    self.database = MySql()
                    mysql_url = self.config['db_url'].replace('mariadb://', 'mysql://')
                    self.connection = self.database.create_connection(mysql_url)
                    
                    if self.connection:
                        progress.console.print("[bold bright_green]■ MySQL connector works (MariaDB-compatible)[/bold bright_green]\n")
                
                if self.connection is None:
                    raise ConnectionError("Failed to connect to database")
                
                self.database.validate_connection(self.connection)
                parsed = urlparse(self.config['db_url'])
                self.database_name = parsed.path.lstrip('/')
                
                progress.update(task, description="[bright_green]● Connection established")
                time.sleep(0.3)
            
            except Exception as e:
                progress.console.print(f"[bold red]✗ Connection failed[/bold red] {str(e)[:100]}")
                raise
        
        # Show connection info
        parsed = urlparse(self.config['db_url'])
        
        self.console.print()
        self.console.print("[bold bright_green]● Connection Established[/bold bright_green]\n")
        self.console.print(f"  [dim]Host    [/dim] [bright_white]{parsed.hostname or 'localhost'}[/bright_white]")
        self.console.print(f"  [dim]Port    [/dim] [bright_white]{parsed.port or 3306}[/bright_white]")
        self.console.print(f"  [dim]Database[/dim] [bright_white]{self.database_name}[/bright_white]")
        self.console.print(f"  [dim]Status  [/dim] [bold bright_green]CONNECTED[/bold bright_green]")
        self.console.print()
    
    def discover_schema(self):
        """Discover database tables with futuristic design"""
        self.console.print()
        self.console.print("[bold bright_cyan]▼ SCHEMA DISCOVERY[/bold bright_cyan]")
        self.console.print(f"[dim]Scanning database '[bright_white]{self.database_name}[/bright_white]'...[/dim]\n")
        
        with Progress(
            SpinnerColumn(style="bright_cyan"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=False
        ) as progress:
            task = progress.add_task("[bright_cyan]Fetching tables...", total=None)
            time.sleep(0.3)
            
            tables_df = self.database.get_table_names(self.connection, self.database_name)
            
            # Handle both uppercase and lowercase column names
            if not tables_df.empty:
                if 'table_name' in tables_df.columns:
                    self.tables = tables_df['table_name'].tolist()
                elif 'TABLE_NAME' in tables_df.columns:
                    self.tables = tables_df['TABLE_NAME'].tolist()
                else:
                    # Try to get the first column as table names
                    self.tables = tables_df.iloc[:, 0].tolist()
            else:
                self.tables = []
            
            progress.update(task, description=f"[bright_cyan]● Found {len(self.tables)} table(s)")
            time.sleep(0.3)
        
        if not self.tables:
            self.console.print("\n[yellow]▲ No tables found[/yellow]\n")
            return
        
        # Display tables in colorful list
        self.console.print()
        self.console.print(f"[bold bright_cyan]● Tables in '{self.database_name}'[/bold bright_cyan]\n")
        
        shapes = ["●", "■", "▲", "◆"]
        colors = ["bright_cyan", "bright_magenta", "bright_green", "bright_yellow"]
        
        for idx, table in enumerate(self.tables, 1):
            shape = shapes[idx % len(shapes)]
            color = colors[idx % len(colors)]
            self.console.print(f"  [bold {color}]{shape}[/bold {color}] [bright_white]{table}[/bright_white]")
        
        self.console.print()
        self.console.print(f"[bold bright_green]✓[/bold bright_green] Discovered [bold yellow]{len(self.tables)}[/bold yellow] table(s)\n")
    
    def initialize_mindsql(self):
        """Initialize MindSQL core"""
        from mindsql.core import MindSQLCore
        
        with self.console.status("[cyan]Initializing MindSQL RAG pipeline...[/cyan]"):
            self.mindsql = MindSQLCore(
                database=self.database,
                vectorstore=self.vectorstore,
                llm=self.llm
            )
            time.sleep(0.5)
        
        self.console.print("[bold green]✓[/bold green] MindSQL RAG pipeline ready!\n")
    
    def index_schema(self):
        """Index DDLs with futuristic design"""
        if not self.tables:
            return
        
        self.console.print()
        self.console.print("[bold bright_magenta]▼ SCHEMA INDEXING[/bold bright_magenta]")
        self.console.print(f"[dim]Preparing to embed {len(self.tables)} table schemas...[/dim]\n")
        
        should_index = Confirm.ask(
            f"[yellow]▶ Index[/yellow] [cyan]{len(self.tables)}[/cyan] [yellow]table schemas into vector store?[/yellow]",
            default=True
        )
        
        if not should_index:
            self.console.print("[yellow]▲ Skipped indexing[/yellow]\n")
            return
        
        self.console.print()
        self.console.print("[bold bright_cyan]● Initializing Embedding Model[/bold bright_cyan]")
        self.console.print(f"  [dim]Model     [/dim] [bright_white]sentence-transformers/all-MiniLM-L6-v2[/bright_white]")
        self.console.print(f"  [dim]Dimension [/dim] [bright_white]384[/bright_white]")
        self.console.print(f"  [dim]Device    [/dim] [bright_white]cpu[/bright_white]")
        self.console.print()
        
        total_chunks = 0
        shapes = ["●", "■", "▲", "◆"]
        colors = ["bright_cyan", "bright_magenta", "bright_green", "bright_yellow"]
        
        with Progress(
            SpinnerColumn(style="bright_magenta"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="bright_magenta", finished_style="bright_green"),
            TextColumn("[bright_magenta]{task.completed}[/bright_magenta]/[bright_white]{task.total}[/bright_white]"),
            console=self.console
        ) as progress:
            task = progress.add_task("[bright_magenta]Embedding schemas...", total=len(self.tables))
            
            for idx, table in enumerate(self.tables, 1):
                try:
                    shape = shapes[idx % len(shapes)]
                    color = colors[idx % len(colors)]
                    progress.update(task, description=f"[bright_magenta]Processing [bright_white]{table}[/bright_white]...")
                    ddl = self.database.get_ddl(self.connection, table)
                    self.vectorstore.index_ddl(ddl, table=table)
                    total_chunks += 1
                    progress.console.print(f"  [bold {color}]{shape}[/bold {color}] [dim]Embedded [{idx}/{len(self.tables)}][/dim] [bright_white]{table}[/bright_white]")
                except Exception as e:
                    progress.console.print(f"  [yellow]▲ Failed {table}[/yellow] [dim]{str(e)[:50]}[/dim]")
                progress.advance(task)
        
        self.console.print()
        self.console.print("[bold bright_green]✓ Schema Indexing Complete[/bold bright_green]\n")
        self.console.print(f"  [dim]Total Chunks  [/dim] [bright_white]{total_chunks}[/bright_white]")
        self.console.print(f"  [dim]Dimensions   [/dim] [bright_white]384[/bright_white]")
        self.console.print(f"  [dim]Storage      [/dim] [bright_white]Vector Database[/bright_white]")
        self.console.print()
    
    def interactive_mode(self):
        """Interactive query mode with futuristic design"""
        self.console.print()
        self.console.print()
        
        # Animated header
        self.console.print("[bold bright_magenta]▼ INTERACTIVE QUERY MODE[/bold bright_magenta]")
        self.console.print("[dim]Natural language to SQL - Real-time processing[/dim]\n")
        
        # Mode information
        self.console.print("[bold bright_cyan]● Active Components[/bold bright_cyan]")
        self.console.print(f"  [dim]Vector Search  [/dim] [bright_white]Enabled[/bright_white]  [dim cyan]• Semantic DDL retrieval[/dim cyan]")
        self.console.print(f"  [dim]LLM Engine     [/dim] [bright_white]Ready[/bright_white]    [dim cyan]• Context-aware SQL generation[/dim cyan]")
        self.console.print(f"  [dim]Database       [/dim] [bright_white]Connected[/bright_white] [dim cyan]• Live query execution[/dim cyan]")
        self.console.print()
        
        # Instructions
        self.console.print("[bold bright_yellow]▶ How to Use[/bold bright_yellow]")
        self.console.print("  [dim]■[/dim] Type your question in natural language")
        self.console.print("  [dim]■[/dim] Press [bright_white]Enter[/bright_white] to execute")
        self.console.print("  [dim]■[/dim] Type [bright_white]'help'[/bright_white] for query examples")
        self.console.print("  [dim]■[/dim] Type [bright_white]'quit'[/bright_white] or [bright_white]'exit'[/bright_white] to stop")
        self.console.print()
        
        # Ready status with animation
        with Progress(
            SpinnerColumn(style="bright_green"),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("[bright_green]Activating interactive mode...", total=None)
            time.sleep(0.5)
        
        self.console.print("[bold bright_green]✓ Interactive Mode Active[/bold bright_green]")
        self.console.print("[dim]─" * 60 + "[/dim]\n")
        
        query_num = 0
        
        while True:
            try:
                question = Prompt.ask("\n[bold bright_yellow]❯[/bold bright_yellow]")
                
                if question.lower() in ['quit', 'exit', 'q']:
                    self.console.print("\n[bold green]Connection closed[/bold green]\n")
                    break
                
                if question.lower() == 'help':
                    self.show_help()
                    continue
                
                if not question.strip():
                    continue
                
                query_num += 1
                
                self.console.print()
                self.console.print(f"[bold bright_cyan]▶ Query #{query_num}[/bold bright_cyan]")
                self.console.print(f"  [dim]Question[/dim] [bright_white]{question}[/bright_white]")
                self.console.print()
                
                start_time = time.time()
                
                # Show progress with spinner
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    # Step 1: Embed query
                    task = progress.add_task("[cyan]Embedding query...[/cyan]", total=None)
                    time.sleep(0.3)
                    
                    # Step 2: Vector search
                    progress.update(task, description="[cyan]Searching vector database...[/cyan]")
                    time.sleep(0.3)
                    
                    # Step 3: Retrieve context
                    progress.update(task, description="[cyan]Retrieving context...[/cyan]")
                    time.sleep(0.2)
                    
                    # Step 4: Generate SQL
                    progress.update(task, description="[cyan]Generating SQL with LLM...[/cyan]")
                    
                    try:
                        # Pass all tables to ensure LLM has full context
                        sql = self.mindsql.create_database_query(
                            question=question,
                            connection=self.connection,
                            tables=self.tables,
                            n_results=10  # Get more context from vector store
                        )
                        progress.update(task, description="[green]✓ SQL generated[/green]")
                    except Exception as e:
                        progress.update(task, description="[red]✗ Error[/red]")
                        progress.stop()
                        self.console.print(f"[red]Error generating SQL: {e}[/red]")
                        continue
                
                # Remove this line - timing shown at end
                
                # Show SQL in cyber-style
                self.console.print()
                self.console.print("[bold bright_green]╔═══ Generated SQL ════════════════════════════════════════╗[/bold bright_green]")
                self.console.print(Panel(
                    Syntax(sql, "sql", theme="monokai", line_numbers=False),
                    border_style="bright_green",
                    padding=(0, 1),
                    title="[bold yellow] ■ SQL Query[/bold yellow]",
                    title_align="left"
                ))
                self.console.print("[bold bright_green]╚══════════════════════════════════════════════════════════╝[/bold bright_green]")
                
                # Execute with progress
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("[cyan]Executing SQL on database...[/cyan]", total=None)
                    result_df = self.database.execute_sql(self.connection, sql)
                    progress.update(task, description="[green]✓ Query executed[/green]")
                
                elapsed = time.time() - start_time
                
                # Show results in colorful table
                self.console.print()
                self.console.print("[bold bright_cyan]╔═══ Query Results ════════════════════════════════════════╗[/bold bright_cyan]")
                
                if result_df.empty:
                    self.console.print("[bold bright_cyan]║[/bold bright_cyan] [yellow]⚠ No results returned[/yellow]")
                else:
                    # Create beautiful colored table
                    result_table = Table(
                        show_header=True,
                        header_style="bold bright_yellow on blue",
                        border_style="bright_cyan",
                        title="[bold bright_magenta] ■ Results[/bold bright_magenta]",
                        title_style="bold bright_magenta",
                        box=box.DOUBLE_EDGE,
                        show_lines=True
                    )
                    
                    # Add columns with colors
                    colors = ["bright_cyan", "bright_magenta", "bright_green", "bright_yellow", "cyan", "magenta"]
                    for idx, col in enumerate(result_df.columns):
                        result_table.add_column(
                            str(col), 
                            style=colors[idx % len(colors)],
                            justify="left"
                        )
                    
                    # Add rows
                    for idx in range(min(10, len(result_df))):
                        row = result_df.iloc[idx]
                        result_table.add_row(*[str(val) for val in row])
                    
                    self.console.print(result_table)
                    
                    if len(result_df) > 10:
                        self.console.print(f"[dim yellow]Showing 10 of {len(result_df)} rows[/dim yellow]")
                    
                    self.console.print()
                    self.console.print(f"[bold bright_green]✓[/bold bright_green] Returned [bold yellow]{len(result_df)}[/bold yellow] rows in [bold cyan]{elapsed:.2f}s[/bold cyan]")
                
                self.console.print("[bold bright_cyan]╚══════════════════════════════════════════════════════════╝[/bold bright_cyan]")
                
                self.console.print()
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Interrupted[/yellow]")
                break
            except EOFError:
                break
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/red]")
    
    def show_help(self):
        """Show help examples with futuristic design"""
        self.console.print()
        self.console.print("[bold bright_yellow]▶ EXAMPLE QUERIES[/bold bright_yellow]\n")
        
        examples = [
            ("●", "bright_cyan", "Show me the customer table"),
            ("■", "bright_green", "How many orders were placed today?"),
            ("▲", "bright_magenta", "List all products with their prices"),
            ("◆", "bright_yellow", "What are the top 5 customers by order count?"),
        ]
        
        if self.tables:
            examples.append(("●", "bright_cyan", f"Show me all records from {self.tables[0]}"))
        
        for shape, color, example in examples:
            self.console.print(f"  [bold {color}]{shape}[/bold {color}] [bright_white]{example}[/bright_white]")
        
        self.console.print()
        self.console.print("[dim]Tip: Ask questions naturally - the AI will understand your intent[/dim]\n")
    
    def run(self):
        """Main execution"""
        try:
            self.show_banner()
            
            # Configuration
            self.config = self.setup_configuration()
            
            # Component selection
            self.select_database()
            self.select_vector_store()
            self.setup_llm()
            
            # Connect
            self.connect_to_database()
            
            # Discover schema
            self.discover_schema()
            
            # Initialize MindSQL
            self.initialize_mindsql()
            
            # Index
            self.index_schema()
            
            # Interactive mode
            self.interactive_mode()
            
            # Cleanup
            if self.connection:
                self.connection.close()
                self.console.print("\n[dim]Connection closed[/dim]\n")
            
            return 0
            
        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]Interrupted by user[/yellow]\n")
            return 1
        except Exception as e:
            self.console.print(f"\n[bold red]Fatal error:[/bold red] {e}\n")
            import traceback
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return 1


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description="MindSQL + MariaDB CLI")
    parser.add_argument("--version", action="version", version="1.0.0")
    args = parser.parse_args()
    
    cli = MindSQLCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
