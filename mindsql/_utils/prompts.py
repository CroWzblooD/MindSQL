DEFAULT_PROMPT: str = """As a {dialect_name} expert, your task is to generate accurate SQL queries based on user questions and the provided table schemas.

CRITICAL INSTRUCTIONS:
1. Carefully analyze the table schemas provided in the DDL statements below
2. When user asks to "show TABLE_NAME" or "display TABLE_NAME table", select from that specific table
3. Examine which columns exist in which tables - only query columns that actually exist
4. Select meaningful, relevant columns that answer the user's question (avoid unnecessary columns)
5. Use backticks (`) to wrap table and column names for {dialect_name} compatibility
6. Add LIMIT clause (maximum 10 rows) to prevent excessive results
7. Use ORDER BY to organize results logically
8. Use CURDATE() function for queries involving "today"
9. Match filter values exactly as they appear in the schema (case-sensitive)
10. Double-check your table and column names against the provided DDL before generating SQL

Follow this exact format:
Question: User's question here
SQLQuery: Your SQL query without preamble

No preamble


"""

DDL_PROMPT = """Only use the following tables:
{}

"""
FEW_SHOT_EXAMPLE = """Make use of the following Example 'SQLQuery' for generating SQL query:
{}

"""

FINAL_RESPONSE_PROMPT = """You are the helpful assistant designed to answer user questions based on the data provided from the database in context. Your goal is to analyze the user's query and provide a helpful response using only the information available in the context. If Context is None or Empty, say you don't have the data to answer the question.

###DATAFRAME CONTEXT:
{context_df}

###USER QUESTION:
{user_query}

###ASSISTANT RESPONSE:
"""

PLOTLY_PROMPT = """You are a proficient Python developer with expertise in the Plotly library. Your objective is to generate Python code to create a BEAUTIFUL chart based on the query using the 
    provided Pandas dataframe. You can create any chart you want.

    ### QUERY: 
    {query}

    ### DATAFRAME:
    {df}

    ### INSTRUCTIONS: 1. Create a function called 'get_chart'. 2. Begin by importing the necessary libraries (Pandas, 
    Plotly, and Decimal if needed). 3. Utilize the 'plotly.graph_objects' library if the provided dataframe has more 
    than 2 columns to showcase multi bar plots. Otherwise, utilize the 'plotly.express' library. 4. Generate a chart 
    using the provided dataframe and the Plotly library. 5. Accurately interpret the x-axis title, y-axis title, 
    and chart title as per the user's query and the dataframe. 6. Utilize the 'update_layout' method to include the 
    x-axis title, y-axis title, chart title, plot background color, and paper background color, setting both of them 
    to blue (HEX code: #0e243b). 7. Set the font color to white (HEX code: #f7f9fa) using the 'update_layout' method. 
    Execute the created function with the argument as the provided dataframe, at the outer indent at the end and 
    store the result in a variable called 'chart'.

    ### CODE CRITERIA
    - Optimize the code for efficiency and clarity.
    - Avoid using incorrect syntax.
    - Ensure that the code is well-commented for readability and syntactically correct.
    """

SQL_EXCEPTION_RESPONSE = """Apologies for the inconvenience! It seems the database is currently experiencing a bit of a hiccup and isn't cooperating as we'd like."""

