import os
import argparse
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, DefaultAzureCredential
from SentinelClient import SentinelClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SentinelMCP')
logger.info("Starting Sentinel MCP Server")
# Load environment variables
load_dotenv()

mcp = FastMCP('SentinelQuery-server')

sentinel_client = None

@mcp.tool()
def run_sentinel_query(query: str) -> str:
    """ Run a query against Sentinel.
    Args:
        query: The Kusto Query Language (KQL) query to run
    Returns:
        Results from the query
    """
    global sentinel_client
    return sentinel_client.run_query(query)
def run_tests():
    """Run test queries to verify functionality."""
    print("[+] Running Sentinel Test")
    sentinel_result = run_sentinel_query("Usage | take 10")
    if sentinel_result.get("status") == "success":
        print("[+] Sentinel Test executed successfully")
    else:
        print("[+] Sentinel Test failed")
def auth(auth_type):  
    """  
    Authenticate with Azure using different credential types based on the provided auth_type.  
    """  
    if auth_type == "interactive":
        credential = InteractiveBrowserCredential()
    elif auth_type == "client_secret":
        credential = ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
    else:
        # Default credential for managed identities
        credential = DefaultAzureCredential()
    # Force authentication to make the user login  
    try:  
        credential.get_token("https://api.loganalytics.io/.default")
    except Exception as e:  
        print(f"Authentication failed: {e}")  
        print("Only unauthenticated tools can be used")  
    return credential      

def create_clients(auth_credential):
    """Create a Sentinel client using environment variables."""
    global sentinel_client

    if sentinel_client is None:
        subscription_id = os.getenv('SENTINEL_SUBSCRIPTION_ID')
        resource_group = os.getenv('SENTINEL_RESOURCE_GROUP')
        workspace_name = os.getenv('SENTINEL_WORKSPACE_NAME')
        workspace_id = os.getenv('SENTINEL_WORKSPACE_ID')
        sentinel_client = SentinelClient(auth_credential, subscription_id, resource_group, workspace_name, workspace_id)
    return sentinel_client

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Sentinel MCP Server")
    parser.add_argument("--run-tests", action="store_true", help="Run tests before starting the server")
    args = parser.parse_args()

    # Create clients
    print("[+] Authenticating using ", os.getenv('AUTHENTICATION_TYPE', 'interactive'))
    auth_credential = auth(os.getenv('AUTHENTICATION_TYPE', 'interactive'))
    create_clients(auth_credential)

    # Run tools test only if specified
    if args.run_tests:
        print("[+] Running tests...")
        run_tests()

    # Run MCP server with SSE transport
    print("[+] Starting MCP server...")
    mcp.run(transport="sse")





