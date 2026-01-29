"""
Advanced Examples for Self-Healing SQL Data Analyst
===================================================

This file demonstrates advanced usage patterns and integration scenarios.
"""

from self_healing_sql_analyst import (
    build_self_healing_analyst,
    AnalystState,
    DatabaseManager,
    Config
)
from langgraph.checkpoint.memory import MemorySaver
import time


# ============================================================================
# EXAMPLE 1: Custom Database Schema
# ============================================================================

def example_custom_database():
    """
    Demonstrate using the analyst with a custom database schema.
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Custom Database Schema")
    print("="*80 + "\n")
    
    # Create custom database
    db = DatabaseManager("custom_sales.db")
    conn = db.db_path
    import sqlite3
    
    conn = sqlite3.connect("custom_sales.db")
    cursor = conn.cursor()
    
    # Create custom schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            segment TEXT,
            country TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Insert sample data
    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)",
        [
            (1, "Acme Corp", "Enterprise", "USA"),
            (2, "TechStart", "SMB", "UK"),
            (3, "Global Inc", "Enterprise", "Germany")
        ]
    )
    
    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?)",
        [
            (1, 1, "2024-01-15", 50000),
            (2, 1, "2024-02-20", 75000),
            (3, 2, "2024-01-10", 15000),
            (4, 3, "2024-03-05", 100000)
        ]
    )
    
    conn.commit()
    conn.close()
    
    print("✓ Custom database created successfully")
    print("\nSchema:")
    print("- customers (customer_id, name, segment, country)")
    print("- orders (order_id, customer_id, order_date, amount)")


# ============================================================================
# EXAMPLE 2: Batch Processing Multiple Questions
# ============================================================================

def example_batch_processing():
    """
    Process multiple questions in batch and compare results.
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Batch Processing")
    print("="*80 + "\n")
    
    questions = [
        "What is the total revenue?",
        "Which region has the highest sales?",
        "What is the average order value?",
        "Show me the top 3 products by revenue"
    ]
    
    # Build graph once
    graph = build_self_healing_analyst()
    app = graph.compile()
    
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Processing: {question}")
        
        initial_state = {
            "question": question,
            "sql_query": "",
            "query_result": "",
            "error_message": "",
            "error_history": [],
            "attempt_count": 0,
            "schema_info": "",
            "explanation": "",
            "status": "pending",
            "timestamp": ""
        }
        
        start_time = time.time()
        result = app.invoke(initial_state)
        elapsed = time.time() - start_time
        
        results.append({
            "question": question,
            "status": result["status"],
            "attempts": result["attempt_count"],
            "time": elapsed,
            "explanation": result["explanation"]
        })
        
        print(f"  Status: {result['status']}")
        print(f"  Attempts: {result['attempt_count']}")
        print(f"  Time: {elapsed:.2f}s")
    
    # Summary
    print("\n" + "="*80)
    print("BATCH PROCESSING SUMMARY")
    print("="*80)
    print(f"Total Questions: {len(questions)}")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'failed')}")
    print(f"Avg Attempts: {sum(r['attempts'] for r in results) / len(results):.1f}")
    print(f"Total Time: {sum(r['time'] for r in results):.2f}s")


# ============================================================================
# EXAMPLE 3: Streaming Progress Updates
# ============================================================================

def example_streaming_progress():
    """
    Demonstrate streaming to show real-time progress.
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Streaming Progress Updates")
    print("="*80 + "\n")
    
    graph = build_self_healing_analyst()
    app = graph.compile()
    
    question = "What was our highest growth region in Q3?"
    
    initial_state = {
        "question": question,
        "sql_query": "",
        "query_result": "",
        "error_message": "",
        "error_history": [],
        "attempt_count": 0,
        "schema_info": "",
        "explanation": "",
        "status": "pending",
        "timestamp": ""
    }
    
    print(f"Question: {question}\n")
    print("Processing Steps:")
    print("-" * 60)
    
    step_count = 0
    for output in app.stream(initial_state):
        step_count += 1
        node_name = list(output.keys())[0]
        node_state = output[node_name]
        
        # Format output based on node type
        if node_name == "initialize":
            print(f"{step_count}. Initializing analysis...")
            print(f"   → Loaded database schema")
        
        elif node_name == "generate_sql":
            print(f"{step_count}. Generating SQL query...")
            sql = node_state.get("sql_query", "")[:60]
            print(f"   → SQL: {sql}...")
        
        elif node_name == "execute_sql":
            if node_state.get("error_message"):
                print(f"{step_count}. Execution failed!")
                print(f"   ⚠ Error: {node_state['error_message'][:50]}...")
            else:
                print(f"{step_count}. Query executed successfully!")
                print(f"   ✓ Retrieved results")
        
        elif node_name == "analyze_error":
            print(f"{step_count}. Self-correcting error...")
            print(f"   → Analyzing failure and generating new SQL")
        
        elif node_name == "generate_explanation":
            print(f"{step_count}. Generating explanation...")
            print(f"   → Creating natural language answer")
        
        elif node_name == "handle_failure":
            print(f"{step_count}. Handling failure...")
            print(f"   ⚠ Max retries exceeded")
        
        time.sleep(0.2)  # Simulate processing time
    
    print("-" * 60)
    print(f"\nCompleted in {step_count} steps")


# ============================================================================
# EXAMPLE 4: State Inspection and Debugging
# ============================================================================

def example_state_inspection():
    """
    Demonstrate detailed state inspection for debugging.
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: State Inspection and Debugging")
    print("="*80 + "\n")
    
    graph = build_self_healing_analyst()
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)
    
    config = {"configurable": {"thread_id": "debug_session"}}
    
    question = "What is the total revenue?"
    
    initial_state = {
        "question": question,
        "sql_query": "",
        "query_result": "",
        "error_message": "",
        "error_history": [],
        "attempt_count": 0,
        "schema_info": "",
        "explanation": "",
        "status": "pending",
        "timestamp": ""
    }
    
    print(f"Question: {question}\n")
    
    # Run analysis
    result = app.invoke(initial_state, config)
    
    # Inspect state history
    print("State History:")
    print("-" * 60)
    
    history = list(app.get_state_history(config))
    
    for i, state in enumerate(reversed(history), 1):
        print(f"\nCheckpoint {i}:")
        print(f"  Next Node: {state.next}")
        print(f"  Status: {state.values.get('status', 'N/A')}")
        print(f"  Attempts: {state.values.get('attempt_count', 0)}")
        
        if state.values.get('sql_query'):
            print(f"  SQL: {state.values['sql_query'][:50]}...")
        
        if state.values.get('error_message'):
            print(f"  Error: {state.values['error_message'][:50]}...")
    
    print("\n" + "-" * 60)
    print(f"Total Checkpoints: {len(history)}")


# ============================================================================
# EXAMPLE 5: Error Recovery Patterns
# ============================================================================

def example_error_recovery():
    """
    Demonstrate different error scenarios and recovery patterns.
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Recovery Patterns")
    print("="*80 + "\n")
    
    # Test different error scenarios
    test_cases = [
        {
            "name": "Invalid Column Name",
            "question": "Show me the invalid_column from sales",
            "expected": "Should detect 'no such column' and correct"
        },
        {
            "name": "Invalid Table Name",
            "question": "Select from nonexistent_table",
            "expected": "Should detect 'no such table' and correct"
        },
        {
            "name": "Complex Aggregation",
            "question": "What is the average revenue per region with growth rate?",
            "expected": "Should handle complex SQL generation"
        }
    ]
    
    graph = build_self_healing_analyst()
    app = graph.compile()
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test['name']}")
        print(f"Question: {test['question']}")
        print(f"Expected: {test['expected']}")
        print("-" * 60)
        
        initial_state = {
            "question": test['question'],
            "sql_query": "",
            "query_result": "",
            "error_message": "",
            "error_history": [],
            "attempt_count": 0,
            "schema_info": "",
            "explanation": "",
            "status": "pending",
            "timestamp": ""
        }
        
        result = app.invoke(initial_state)
        
        print(f"Result Status: {result['status']}")
        print(f"Attempts Made: {result['attempt_count']}")
        print(f"Errors Encountered: {len(result['error_history'])}")
        
        if result['error_history']:
            print("\nError History:")
            for j, error in enumerate(result['error_history'], 1):
                print(f"  {j}. {error[:60]}...")
        
        print()


# ============================================================================
# EXAMPLE 6: Performance Monitoring
# ============================================================================

def example_performance_monitoring():
    """
    Monitor and analyze system performance metrics.
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Performance Monitoring")
    print("="*80 + "\n")
    
    questions = [
        "What is the total revenue?",
        "Which product sold the most units?",
        "What is the average revenue per quarter?",
        "Show me sales trends by region"
    ]
    
    graph = build_self_healing_analyst()
    app = graph.compile()
    
    metrics = {
        "total_time": 0,
        "successful_queries": 0,
        "failed_queries": 0,
        "total_attempts": 0,
        "retries_needed": 0,
        "avg_time_per_query": 0
    }
    
    print("Running performance tests...\n")
    
    for question in questions:
        initial_state = {
            "question": question,
            "sql_query": "",
            "query_result": "",
            "error_message": "",
            "error_history": [],
            "attempt_count": 0,
            "schema_info": "",
            "explanation": "",
            "status": "pending",
            "timestamp": ""
        }
        
        start = time.time()
        result = app.invoke(initial_state)
        elapsed = time.time() - start
        
        metrics["total_time"] += elapsed
        metrics["total_attempts"] += result["attempt_count"]
        
        if result["status"] == "success":
            metrics["successful_queries"] += 1
        else:
            metrics["failed_queries"] += 1
        
        if result["attempt_count"] > 1:
            metrics["retries_needed"] += 1
    
    metrics["avg_time_per_query"] = metrics["total_time"] / len(questions)
    
    # Display metrics
    print("="*60)
    print("PERFORMANCE METRICS")
    print("="*60)
    print(f"Total Queries: {len(questions)}")
    print(f"Successful: {metrics['successful_queries']}")
    print(f"Failed: {metrics['failed_queries']}")
    print(f"Success Rate: {metrics['successful_queries']/len(questions)*100:.1f}%")
    print(f"\nTotal Attempts: {metrics['total_attempts']}")
    print(f"Queries Needing Retry: {metrics['retries_needed']}")
    print(f"Avg Attempts per Query: {metrics['total_attempts']/len(questions):.2f}")
    print(f"\nTotal Time: {metrics['total_time']:.2f}s")
    print(f"Avg Time per Query: {metrics['avg_time_per_query']:.2f}s")


# ============================================================================
# EXAMPLE 7: Integration with External LLM
# ============================================================================

def example_openai_integration():
    """
    Demonstrate integration with OpenAI GPT models.
    Note: Requires OPENAI_API_KEY environment variable.
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: OpenAI Integration (Mock)")
    print("="*80 + "\n")
    
    print("To integrate with OpenAI:")
    print("""
    1. Install: pip install langchain-openai
    
    2. Update LLMService class:
    
    from langchain_openai import ChatOpenAI
    
    class LLMService:
        def __init__(self):
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0
            )
        
        def generate_sql(self, question, schema, error_context=None):
            messages = [
                {
                    "role": "system",
                    "content": f"You are a SQL expert. Database schema:\\n{schema}"
                },
                {
                    "role": "user",
                    "content": f"Generate SQL for: {question}"
                }
            ]
            
            if error_context:
                messages.append({
                    "role": "assistant",
                    "content": f"Previous errors: {error_context}"
                })
            
            response = self.llm.invoke(messages)
            return response.content
    
    3. Set environment variable:
       export OPENAI_API_KEY='your-api-key'
    """)


# ============================================================================
# MAIN RUNNER
# ============================================================================

if __name__ == "__main__":
    """
    Run all advanced examples
    """
    
    examples = [
        ("Custom Database", example_custom_database),
        ("Batch Processing", example_batch_processing),
        ("Streaming Progress", example_streaming_progress),
        ("State Inspection", example_state_inspection),
        ("Error Recovery", example_error_recovery),
        ("Performance Monitoring", example_performance_monitoring),
        ("OpenAI Integration", example_openai_integration),
    ]
    
    print("\n" + "#"*80)
    print("ADVANCED EXAMPLES - SELF-HEALING SQL DATA ANALYST")
    print("#"*80)
    
    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\n⚠ Example {i} ({name}) encountered an error: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "#"*80)
    print("ALL EXAMPLES COMPLETED")
    print("#"*80)
    print("\nKey Takeaways:")
    print("- Self-correction enables resilient systems")
    print("- State management provides full observability")
    print("- Streaming enables real-time feedback")
    print("- Checkpointing enables debugging and replay")
    print("- Batch processing enables scale")
