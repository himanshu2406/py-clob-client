
import os
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_clob_client.constants import AMOY

def count_markets():
    try:
        # Minimal init - keys not needed for public endpoints usually, 
        # but py-clob-client checks for them in __init__ if we want L1/L2?
        # Actually L0 is fine for public endpoints.
        host = "https://clob.polymarket.com"
        client = ClobClient(host) 
        
        print("Fetching markets...")
        # Use simple get_markets loop
        next_cursor = "MA=="
        count = 0
        pages = 0
        
        while next_cursor != "LTE=": # DELETE_ME: END_CURSOR
            resp = client.get_markets(next_cursor=next_cursor)
            # Response is list or dict? client.py says:
            # return get("{}{}?next_cursor={}".format(self.host, GET_MARKETS, next_cursor))
            # Usually returns {"data": [...], "next_cursor": ...}
            
            # Use raw request to be safe if client helper obscures it
            # But let's trust client first. 
            # Wait, client.get_markets returns the raw get() result.
            
            if "data" not in resp:
                print("Unexpected response structure:", resp.keys())
                break
                
            batch_len = len(resp["data"])
            count += batch_len
            next_cursor = resp.get("next_cursor")
            pages += 1
            print(f"Page {pages}: {batch_len} markets. Total so far: {count}")
            
            if pages > 5: # Safety break for testing
                print("Stopping early for test.")
                break
                
        print(f"Total Markets Found: {count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    count_markets()
