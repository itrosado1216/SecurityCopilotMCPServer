# Sentinel MCP Server

A Python-based MCP server using the FastMCP library that executes KQL queries against a Log Analytics workspace using Azure Identity authentication.
## Overview

This project implements a minimal MCP server that enables:

- Running KQL queries against Microsoft Sentinel

The server acts as a bridge between development environments and Microsoft Sentinel, allowing for testing and execution of KQL queries. It uses SSE as the transport layer for the MCP server.
## Features

- **Sentinel Integration**: Execute KQL queries against your Log Analytics workspace
- **Authentication Support**: Multiple authentication methods including interactive browser, client secret, and managed identity
## Prerequisites

- Python 3.8+
- Microsoft Sentinel workspace
- Appropriate Azure permissions for Sentinel

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jguimera/SecurityCopilotMCPServer.git
   cd SecurityCopilotMCPServer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following configuration:
   ```
   #Add App Reg to use ClientID and Secret authentication
   #AZURE_TENANT_ID=your_tenant_id
   #AZURE_CLIENT_ID=your_client_id
   #AZURE_CLIENT_SECRET=your_client_secret
   SENTINEL_SUBSCRIPTION_ID=your_subscription_id
   SENTINEL_RESOURCE_GROUP=your_resource_group
   SENTINEL_WORKSPACE_NAME=your_workspace_name
   SENTINEL_WORKSPACE_ID=your_workspace_id
   #Authentication Options: interactive, client_secret
   AUTHENTICATION_TYPE=interactive
   ```

## Usage

### Starting the Server

Run the MCP server:

```
python server.py
```

To run tests before starting the server:

```
python server.py --run-tests
```

### Available Tools

The MCP server provides the following tool:

1. **run_sentinel_query**: Execute KQL queries in Sentinel

### MCP Client Config for Cursor
You can use this MCP server from the client of your choice. The `.cursor` folder contains the `mcp.json` file to connect Cursor to the MCP server.

You can invoke the tool directly using `/tool_name parameter1="Value"`.

More info: https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
