
import asyncio
import websockets
import json

async def test_public_wss():
    uris = [
        "wss://ws-subscriptions-clob.polymarket.com/ws/market",
        "wss://ws-subscriptions-clob.polymarket.com/ws/",
        "wss://ws-live-data.polymarket.com/ws/" # RTDS just in case
    ]
    
    for uri in uris:
        print(f"--- Connecting to {uri} ---")
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to {uri}.")
                
                # Try to subscribe
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
    asyncio.run(test_public_wss())
