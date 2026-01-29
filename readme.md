# Context Engineering in Self-Healing SQL Data Analyst

## What is Context Engineering?

**Context Engineering** is the practice of intelligently building, selecting, and formatting contextual information to provide to Large Language Models (LLMs) for optimal performance. It's like preparing a comprehensive briefing package for an expert before they tackle a complex problem.

## Why Context Engineering Matters

Without proper context, LLMs may:
- Generate incorrect SQL syntax
- Reference non-existent tables or columns
- Miss business-specific conventions
- Fail to understand data patterns
- Make the same mistakes repeatedly

With effective context engineering, LLMs:
- Generate more accurate queries on the first attempt
- Follow company-specific conventions automatically
- Learn from past successes and failures
- Understand data relationships better
- Self-correct more intelligently

## Context Engineering Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUESTION                             │
│              "What was our highest growth                    │
│               region in Q3?"                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT ENGINEER                                │
│  Builds rich, multi-layered context package                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─────► 1. SCHEMA CONTEXT
                       │       - Table structures
                       │       - Column types & constraints
                       │       - Indexes and keys
                       │
                       ├─────► 2. RELATIONSHIP CONTEXT
                       │       - Foreign key relationships
                       │       - Join patterns
                       │       - Entity connections
                       │
                       ├─────► 3. BUSINESS CONTEXT
                       │       - Domain rules
                       │       - Naming conventions
                       │       - Common metrics
                       │
                       ├─────► 4. QUERY EXAMPLES
                       │       - Few-shot examples
                       │       - Pattern library
                       │       - Best practices
                       │
                       ├─────► 5. DATA SAMPLES
                       │       - Example records
                       │       - Data formats
                       │       - Value ranges
                       │
                       ├─────► 6. STATISTICS
                       │       - Column cardinality
                       │       - Min/max values
                       │       - Distribution info
                       │
                       ├─────► 7. QUERY HISTORY
                       │       - Past successes
                       │       - Pattern learning
                       │       - User preferences
                       │
                       └─────► 8. ERROR CONTEXT
                               - Previous failures
                               - Correction patterns
                               - What to avoid
                       
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 CONTEXT-RICH PROMPT                          │
│  Comprehensive briefing for LLM to generate accurate SQL     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM (GPT-4, Claude, etc.)                 │
│  Generates SQL with deep understanding                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
                  HIGH-QUALITY SQL
```

## Implementation Details

### 1. Schema Context

**Purpose**: Provide complete understanding of database structure

**Components**:
```python
- Table names and descriptions
- Column names, types, and constraints
- Primary and foreign keys
- Index information
- Schema annotations
```

**Example Output**:
```
DATABASE SCHEMA CONTEXT:
============================================================

Table: sales
Columns:
  - id (INTEGER) PRIMARY KEY
  - region (TEXT) NOT NULL
  - product (TEXT) NOT NULL
  - revenue (REAL) NOT NULL
  - units_sold (INTEGER) NOT NULL
  - quarter (TEXT) NOT NULL
  - year (INTEGER) NOT NULL

SCHEMA NOTES:
- All tables use INTEGER PRIMARY KEY
- Date fields are stored as TEXT in ISO format
- Monetary values are REAL (floating point)
```

### 2. Relationship Context

**Purpose**: Help LLM understand how to join tables correctly

**Components**:
```python
- Foreign key relationships
- Common join patterns
- Entity relationship descriptions
```

**Example Output**:
```
TABLE RELATIONSHIPS:
============================================================

Table: orders
  - customer_id → customers.customer_id
  - product_id → products.product_id

Common Joins:
- Orders + Customers: ON orders.customer_id = customers.id
- Orders + Products: ON orders.product_id = products.id
```

### 3. Business Context

**Purpose**: Encode domain-specific rules and conventions

**Components**:
```python
- Business rules and policies
- Naming conventions
- Common metrics and calculations
- Domain terminology
```

**Example Output**:
```
BUSINESS CONTEXT:
============================================================

Domain: Sales Analytics

Business Rules:
1. Quarters are labeled as 'Q1', 'Q2', 'Q3', 'Q4'
2. Revenue is always in USD
3. Regions: North America, Europe, Asia
4. Fiscal year aligns with calendar year
5. Growth rate = (New - Old) / Old * 100

Common Metrics:
- Total Revenue: SUM(revenue)
- Average Deal Size: AVG(revenue)
- Units Sold: SUM(units_sold)
- Revenue per Unit: revenue / units_sold

Naming Conventions:
- Use lowercase for column names
- Use snake_case for multi-word names
- Always use table aliases in joins
```

### 4. Few-Shot Examples

**Purpose**: Teach LLM the expected query patterns through examples

**Components**:
```python
- Question-SQL pairs
- Pattern explanations
- Best practice demonstrations
```

**Example Output**:
```
QUERY EXAMPLES:
============================================================

Example 1:
Question: What is the total revenue?
SQL:
SELECT SUM(revenue) as total_revenue FROM sales;
Note: Use SUM aggregation for totals

Example 2:
Question: Which region has the highest sales?
SQL:
SELECT region, SUM(revenue) as total
FROM sales
GROUP BY region
ORDER BY total DESC
LIMIT 1;
Note: Use GROUP BY for aggregation by category, ORDER BY for sorting
```

### 5. Data Samples

**Purpose**: Show actual data patterns and formats

**Components**:
```python
- Sample rows from tables
- Data format examples
- Typical value ranges
```

**Example Output**:
```
SAMPLE DATA:
============================================================

Table: sales
----------------------------------------
id | region | product | revenue | units_sold | quarter | year
----------------------------------------
1 | North America | Product A | 150000 | 500 | Q3 | 2024
2 | North America | Product B | 200000 | 600 | Q3 | 2024
3 | Europe | Product A | 180000 | 550 | Q3 | 2024
```

### 6. Column Statistics

**Purpose**: Provide insights into data distributions

**Components**:
```python
- Distinct value counts
- Min/max ranges
- Null percentages
- Cardinality information
```

**Example Output**:
```
COLUMN STATISTICS:
============================================================

Table: sales
  - region (TEXT): 3 distinct values out of 9 rows
  - product (TEXT): 2 distinct values out of 9 rows
  - revenue (REAL): 9 distinct values, range: [140000, 300000]
  - units_sold (INTEGER): 9 distinct values, range: [480, 900]
  - quarter (TEXT): 2 distinct values out of 9 rows
  - year (INTEGER): 1 distinct values out of 9 rows
```

### 7. Query History

**Purpose**: Learn from past successful queries

**Components**:
```python
- Previous question-SQL pairs
- Successful pattern library
- User-specific preferences
```

**Example Output**:
```
RECENT SUCCESSFUL QUERIES:
============================================================

1. Question: What is the total revenue?
   SQL: SELECT SUM(revenue) as total_revenue FROM sales...

2. Question: Which region performs best?
   SQL: SELECT region, SUM(revenue) as total FROM sales...
```

### 8. Error Context

**Purpose**: Learn from failures to avoid repeated mistakes

**Components**:
```python
- Previous error messages
- Failed query attempts
- Correction patterns
```

**Example Output**:
```
PREVIOUS ERRORS (AVOID THESE):
============================================================

1. SQL Error: no such column: invalid_column
   - Avoid referencing columns not in schema
   - Always verify column names against schema

2. SQL Error: syntax error near 'FROM'
   - Check SQL syntax carefully
   - Follow example patterns
```

## Intelligent Context Selection

The `ContextEngineer` class intelligently selects which context to include based on the question:

```python
def create_prompt_context(self, question: str, error_context: list = None) -> str:
    """
    Create optimized prompt context for SQL generation.
    
    This intelligently selects and formats context based on the question.
    """
    full_context = self.build_full_context()
    
    prompt = "You are an expert SQL analyst..."
    
    # Always include schema
    prompt += full_context["schema"]
    
    # Add relationships if question involves multiple tables
    if any(word in question.lower() for word in ["join", "with", "and", "across"]):
        prompt += full_context["relationships"]
    
    # Add business rules
    prompt += full_context["business_rules"]
    
    # Add examples for complex queries
    if any(word in question.lower() for word in ["growth", "compare", "trend", "rate"]):
        prompt += full_context["examples"]
    
    # Add data samples
    prompt += full_context["data_samples"]
    
    # Add statistics for aggregation queries
    if any(word in question.lower() for word in ["average", "total", "sum", "count"]):
        prompt += full_context["statistics"]
    
    # Add query history
    prompt += full_context["query_history"]
    
    # Add error context for self-correction
    if error_context:
        prompt += format_error_context(error_context)
    
    return prompt
```

## Benefits of Context Engineering

### 1. Improved First-Time Success Rate
- **Without Context**: 40-60% success rate
- **With Context**: 80-95% success rate

### 2. Faster Self-Correction
- **Without Context**: Averages 2-3 attempts per correction
- **With Context**: Averages 1-2 attempts per correction

### 3. Better Business Alignment
- Automatically follows company conventions
- Uses correct terminology and metrics
- Respects business rules

### 4. Continuous Learning
- Builds pattern library over time
- Learns from successes and failures
- Adapts to user preferences

### 5. Reduced Token Usage
- More efficient prompts
- Better relevance
- Less trial and error

## Best Practices

### 1. Keep Context Fresh
```python
# Regularly update statistics
context_engineer.refresh_statistics()

# Clear old history
if len(query_cache) > MAX_HISTORY:
    query_cache = query_cache[-MAX_HISTORY:]
```

### 2. Balance Context Size
```python
# Don't overwhelm with too much context
MAX_SCHEMA_TOKENS = 2000
MAX_EXAMPLES = 5
MAX_HISTORY = 10
```

### 3. Prioritize Relevance
```python
# Include only relevant context
if "join" in question:
    include_relationships = True
else:
    include_relationships = False
```

### 4. Cache Expensive Operations
```python
# Cache schema and statistics
@lru_cache(maxsize=1)
def get_schema_context():
    return build_schema()
```

### 5. Version Your Context
```python
# Track context versions for reproducibility
context = {
    "version": "1.0",
    "generated_at": timestamp,
    "components": {...}
}
```

## Measuring Context Engineering Effectiveness

### Key Metrics

1. **First-Attempt Success Rate**
   ```python
   success_rate = successful_first_attempts / total_attempts
   ```

2. **Average Attempts to Success**
   ```python
   avg_attempts = total_attempts / successful_queries
   ```

3. **Error Reduction Over Time**
   ```python
   error_trend = errors_this_period / errors_last_period
   ```

4. **Context Relevance Score**
   ```python
   relevance = used_context_components / provided_context_components
   ```

## Integration with Production LLMs

### OpenAI GPT-4

```python
from langchain_openai import ChatOpenAI

class LLMService:
    def __init__(self, context_engineer):
        self.context_engineer = context_engineer
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    def generate_sql(self, question, schema, error_context=None):
        # Build rich context
        prompt = self.context_engineer.create_prompt_context(
            question, 
            error_context
        )
        
        # Call LLM with context
        response = self.llm.invoke([
            {"role": "system", "content": "You are an expert SQL analyst."},
            {"role": "user", "content": prompt}
        ])
        
        return response.content
```

### Anthropic Claude

```python
from langchain_anthropic import ChatAnthropic

class LLMService:
    def __init__(self, context_engineer):
        self.context_engineer = context_engineer
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    def generate_sql(self, question, schema, error_context=None):
        prompt = self.context_engineer.create_prompt_context(
            question,
            error_context
        )
        
        response = self.llm.invoke(prompt)
        return response.content
```

## Conclusion

Context Engineering is the foundation of high-performance LLM applications. By providing comprehensive, relevant, and well-structured context, we enable LLMs to:

1. Generate more accurate outputs on the first attempt
2. Self-correct more intelligently when errors occur
3. Follow domain-specific conventions automatically
4. Learn and improve continuously
5. Provide more reliable, production-ready results

The Self-Healing SQL Data Analyst demonstrates these principles in action, showing how context engineering transforms a basic SQL generator into an intelligent, resilient, self-improving system.

---

**Key Takeaway**: Context is to LLMs what knowledge is to humans. The richer and more relevant the context, the better the performance.
