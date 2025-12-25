
import asyncio
import websockets
import json

async def test_public_wss_ua():
    uri = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    # Try adding User-Agent
    extra_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Origin": "https://polymarket.com"
    }
    
    print(f"--- Connecting to {uri} with Headers ---")
    try:
        async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
            print(f"Connected to {uri}.")
            
            msg = {
                "type": "MARKET",
                "assets_ids": ["210668f5feb0"], 
                "auth": {} 
            }
            print(f"Sending: {msg}")
            await websocket.send(json.dumps(msg))
            
            print("Waiting for response...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Response: {response}")
            except asyncio.TimeoutError:
                print("Timeout waiting for response.")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_public_wss_ua())
