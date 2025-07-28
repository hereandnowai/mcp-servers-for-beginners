# Project 10: Multi-Agent Coordinator

This project demonstrates a simple multi-agent system where two agents coordinate their actions through a shared MCP server.

Agent 1 performs a calculation and stores the result on the server.
Agent 2 waits for the result, retrieves it, and then performs another action.

## How to run

1.  Start the server:
    ```bash
    python server.py
    ```
2.  In a new terminal, run Agent 1:
    ```bash
    python agent1.py
    ```
3.  In another new terminal, run Agent 2:
    ```bash
    python agent2.py
    ```

## Expected Output

You will see the agents communicating through the server in their respective terminals.

**Agent 1 Terminal:**
```
Agent 1: Performing a complex calculation...
Agent 1: Calculation complete. Result is [some number].
Agent 1: Storing result on the server.
Agent 1: Server response: Value set for key 'calculation_result'.
```

**Agent 2 Terminal:**
```
Agent 2: Waiting for result from Agent 1...
Agent 2: Result not ready yet. Waiting...
Agent 2: Got result from Agent 1: [some number]
Agent 2: Performing another action with the result.
Agent 2: Final result is [some number * 2].
```
