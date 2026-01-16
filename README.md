# 🎯 GMGN.ai Top Traders Scraper - 100+ Traders

## 📋 Overview

This repository contains a complete solution to extract **ALL 100+ Top Traders** from GMGN.ai using authenticated API calls.

## ✨ Features

- ✅ **Extracts ALL 100 traders** (not just visible ones)
- ✅ **Authenticated API calls** using browser session
- ✅ **Complete data extraction** including:
  - Wallet addresses and links
  - Profit/loss data
  - Trading volumes
  - Transaction counts
  - Balance information
  - Wallet tags
- ✅ **Visible browser** for monitoring
- ✅ **Robust error handling**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/metapsych/gmgn100t.git
cd gmgn100t

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Run the scraper
python3 scrape_all_traders.py
```

## 📁 Files

- `scrape_all_traders.py` - Main scraper script
- `README.md` - This documentation
- `requirements.txt` - Python dependencies

## 🔧 Requirements

- Python 3.8+
- Playwright browser automation
- Valid GMGN.ai login session

## 📊 Output

The scraper creates `all_traders.json` with complete data for all 100+ traders.

## 🛠️ How It Works

1. **Opens browser** with saved GMGN.ai session
2. **Navigates** to the token page
3. **Clicks** "Top Traders" tab
4. **Monitors** network requests to find API endpoint
5. **Calls** API with browser authentication
6. **Extracts** all 100+ traders
7. **Saves** complete dataset

## 📄 Data Fields

Each trader includes:
- `rank` - Position in ranking (1-100+)
- `wallet` - Wallet address
- `wallet_link` - Full URL to wallet page
- `profit` - Total profit/loss in USD
- `realized_profit` - Realized gains
- `unrealized_profit` - Unrealized gains
- `buy_volume_cur` - Current buy volume
- `sell_volume_cur` - Current sell volume
- `buy_tx_count_cur` - Buy transactions
- `sell_tx_count_cur` - Sell transactions
- `native_balance` - Token balance
- `wallet_tag_v2` - Wallet classification tags
- And 15+ more fields!

## ⚠️ Important Notes

- **Login Required**: You must be logged into GMGN.ai first
- **Session Storage**: Browser saves login session automatically
- **Rate Limiting**: Be mindful of API call frequency
- **Authentication**: Uses existing browser cookies/tokens

## 🔍 Troubleshooting

### If no traders are extracted:
1. Check if you're logged into GMGN.ai
2. Verify the token address is correct
3. Check browser console for errors
4. Ensure network connectivity

### If browser doesn't open:
1. Install Playwright: `playwright install chromium`
2. Check system dependencies
3. Verify Python version (3.8+)

## 📞 Support

For issues or questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section
- Review browser console logs

---

**🎯 Mission**: Extract complete Top Traders data from GMGN.ai  
**📊 Result**: All 100+ traders with full trading data  
**🔧 Method**: Authenticated API calls via browser context