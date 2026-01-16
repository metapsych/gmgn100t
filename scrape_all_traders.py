#!/usr/bin/env python3
"""
GMGN.ai Top Traders Scraper - Extract ALL 100+ Traders
Uses authenticated browser context to call API directly
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

async def scrape_all_traders():
    print("\n" + "="*70)
    print("  🎯 GMGN.AI TOP TRADERS SCRAPER")
    print("="*70)
    print("\nThis script extracts ALL 100+ Top Traders from GMGN.ai")
    print("Using authenticated API calls via browser context")
    print("\nPress Enter to start...")
    input()
    
    # Token address (can be changed as needed)
    token_address = "BTyjf4y7sLXgtahZCH6X7gGRnGgYqRFyBSDjL6u6pump"
    
    # Output file
    output_file = "all_traders.json"
    
    print(f"\n🎯 Target Token: {token_address}")
    print(f"📁 Output File: {output_file}")
    
    try:
        async with async_playwright() as p:
            print("\n🚀 Launching browser with saved session...")
            
            # Launch with persistent context (uses saved login session)
            context = await p.chromium.launch_persistent_context(
                user_data_dir="./browser_data/gmgn_session",
                headless=False,  # Visible browser
                viewport={'width': 1920, 'height': 1080},
                args=['--disable-blink-features=AutomationControlled']
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("✅ Browser launched with authenticated session")
            
            # Navigate to token page
            print(f"\n📄 Loading token page...")
            url = f"https://gmgn.ai/sol/token/{token_address}"
            await page.goto(url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Click Top Traders tab
            print("\n🖱️ Clicking 'Top Traders' tab...")
            try:
                await page.click('#traders', timeout=10000)
                print("✅ Tab clicked successfully")
                await asyncio.sleep(5)  # Wait for API call
            except Exception as e:
                print(f"⚠️ Could not click tab: {e}")
                print("💡 Please click 'Top Traders' tab manually")
                print("   Waiting 15 seconds...")
                await asyncio.sleep(15)
            
            # Call API using browser authentication
            print("\n📡 Calling Top Traders API...")
            api_url = f"https://gmgn.ai/vas/api/v1/token_traders/sol/{token_address}"
            
            result = await page.evaluate(f"""
                async () => {{
                    try {{
                        console.log('📡 Making API call to: {api_url}');
                        const response = await fetch('{api_url}');
                        const data = await response.json();
                        console.log('✅ API Response:', data);
                        return {{ success: true, status: response.status, data: data }};
                    }} catch (error) {{
                        console.log('❌ API Error:', error);
                        return {{ success: false, error: error.toString() }};
                    }}
                }}
            """)
            
            if result.get('success') and result.get('status') == 200:
                print("✅ API call successful!")
                traders_data = result['data']
                
                # Extract traders from response
                traders = extract_traders_from_response(traders_data)
                
                if traders:
                    print(f"\n🎉 SUCCESS! Extracted {len(traders)} traders!")
                    
                    # Sort by rank
                    traders.sort(key=lambda x: x.get('rank', 999))
                    
                    # Save complete dataset
                    output_data = {
                        'extraction_info': {
                            'total_traders': len(traders),
                            'token_address': token_address,
                            'extraction_method': 'Authenticated API via browser context',
                            'timestamp': asyncio.get_event_loop().time()
                        },
                        'traders': traders
                    }
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"\n💾 Saved: {output_file}")
                    
                    # Show statistics
                    print(f"\n📊 Extraction Statistics:")
                    print(f"   Total traders: {len(traders)}")
                    
                    if traders:
                        ranks = [t.get('rank', 0) for t in traders]
                        profits = [t.get('profit', 0) for t in traders if t.get('profit')]
                        
                        if ranks:
                            print(f"   Rank range: {min(ranks)} to {max(ranks)}")
                        if profits:
                            print(f"   Profit range: ${min(profits):.2f} to ${max(profits):.2f}")
                    
                    # Show sample traders
                    print(f"\n📋 Sample (first 5 traders):")
                    for i, trader in enumerate(traders[:5], 1):
                        rank = trader.get('rank', 'N/A')
                        wallet = trader.get('wallet', 'N/A')[:20]
                        profit = trader.get('profit', 0)
                        print(f"   {i}. Rank {rank}: {wallet}... | Profit: ${profit:,.2f}")
                    
                    return True
                else:
                    print("❌ Could not extract traders from API response")
                    return False
            else:
                print(f"❌ API call failed: {result}")
                return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def extract_traders_from_response(data):
    """Extract traders from various API response formats"""
    
    traders = []
    
    if isinstance(data, dict):
        # Look for traders in common keys
        for key in ['data', 'traders', 'result', 'items']:
            if key in data:
                potential = data[key]
                
                # Handle nested structures
                if isinstance(potential, dict):
                    for subkey in ['traders', 'list', 'items']:
                        if subkey in potential:
                            potential = potential[subkey]
                            break
                
                # Check if we found a list of traders
                if isinstance(potential, list) and potential:
                    first_item = potential[0]
                    if isinstance(first_item, dict):
                        # Check for trader-like fields
                        trader_fields = ['wallet', 'address', 'wallet_address', 'rank', 'profit']
                        if any(field in first_item for field in trader_fields):
                            traders = potential
                            break
    
    elif isinstance(data, list):
        # Direct list of traders
        if data and isinstance(data[0], dict):
            traders = data
    
    # Normalize trader data
    normalized_traders = []
    for i, trader in enumerate(traders, 1):
        normalized = {
            'rank': trader.get('rank', i),
            'wallet': trader.get('wallet') or trader.get('address') or trader.get('wallet_address'),
            'wallet_link': f"https://gmgn.ai/sol/address/{trader.get('wallet') or trader.get('address') or trader.get('wallet_address')}" if trader.get('wallet') or trader.get('address') or trader.get('wallet_address') else None,
        }
        
        # Copy all other fields
        for key, value in trader.items():
            if key not in normalized:
                normalized[key] = value
        
        normalized_traders.append(normalized)
    
    return normalized_traders

def main():
    """Main function with error handling"""
    try:
        success = asyncio.run(scrape_all_traders())
        
        if success:
            print("\n" + "="*70)
            print("  ✨ EXTRACTION COMPLETE!")
            print("="*70)
            print(f"\n📁 File created: all_traders.json")
            
            # Show final stats
            try:
                with open('all_traders.json', 'r') as f:
                    data = json.load(f)
                    print(f"📊 Ready to use with {len(data['traders'])} traders")
            except:
                pass
        else:
            print("\n" + "="*70)
            print("  ❌ EXTRACTION FAILED")
            print("="*70)
            print("\n💡 Troubleshooting:")
            print("   1. Ensure you're logged into GMGN.ai")
            print("   2. Check browser_data/gmgn_session exists")
            print("   3. Try running browser manually first")
            print("   4. Check token address is correct")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Extraction cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    main()