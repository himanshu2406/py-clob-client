
import asyncio
import websockets
import json
import os
from py_clob_client.client import ClobClient

async def run_demo():
    print("--- Polymarket Live Data Demo (10 Markets) ---")
    
    # 1. Fetch Active Markets via REST
    print("Fetching markets from REST API...")
    host = "https://clob.polymarket.com"
    client = ClobClient(host) # Public access for get_markets
    
    try:
        resp = client.get_markets()
        # client.get_markets() calls the endpoint which typically returns a pagination wrapper
        # The structure is usually {"data": [...], "next_cursor": ...}
        # Let's handle both raw list or dict wrapper just in case, but based on client.py it returns raw GET result.
        
        markets = resp.get("data", []) if isinstance(resp, dict) else resp
        
        if not markets:
            print("No markets found!")
            return

        # Take top 10
        demo_markets = markets[:10]
        print(f"Got {len(demo_markets)} markets for demo.")
        
        # Extract IDs (condition_id is usually used for market channel)
        # Check structure: 'condition_id' or 'token_id'?
        # Docs say 'asset_ids' for subscription. 
        # For 'market' channel, it's often the condition_id or the specific asset_id (token_id).
        # Let's try condition_id first, as it maps to the market. 
        # Actually, search result said: "assets_ids": An array of asset IDs (token IDs)
        # So we should look for 'tokens' in the market data and get the token_id.
        
        asset_ids = []
        for m in demo_markets:
            # Each market has 2 tokens (Yes/No) usually. 
            # Structure might be m['tokens'] -> [{'token_id': ...}, ...]
            if 'tokens' in m:
                for t in m['tokens']:
                    if 'token_id' in t:
                        asset_ids.append(t['token_id'])
            elif 'token_id' in m:
                 asset_ids.append(m['token_id'])
                 
        # Limit total assets to 10-20 to keep it clean
        asset_ids = asset_ids[:10]
        print(f"Subscribing to {len(asset_ids)} assets: {asset_ids}")

    except Exception as e:
        print(f"Error fetching markets: {e}")
        return

    # 2. Connect to WebSocket
    uri = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Origin": "https://polymarket.com"
    }
    
    print(f"Connecting to WSS: {uri}")
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        print("Connected.")
        
        # 3. Subscribe
        msg = {
            "type": "MARKET",
            "assets_ids": asset_ids,
            "auth": {} # Public access
        }
        await websocket.send(json.dumps(msg))
        print("Subscription sent.")
        
        # 4. Listen
        print("Listening for updates (Ctrl+C to stop)...")
        try:
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                # Pretty print concise info
                if isinstance(data, list):
                    for item in data:
                        print(f"Update: {item.get('event_type')} | ID: {item.get('asset_id')} | Price: {item.get('price')}")
                else:
                    print(f"Event: {data}")
                    
        except asyncio.CancelledError:
            print("Stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\nExiting...")
