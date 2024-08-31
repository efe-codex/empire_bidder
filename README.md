
---

# Empire Bidder

**Disclaimer:** Use at your own risk.

## Getting Started

### 0. Download files, install Python and download required modules [HOW TO INSTALL](HOWTOINSTALL.md).

### 1. Update Price Data
Ensure you have the latest price data for all items. This should be stored in a `prices.json` file in the correct format. I recommend using the Pricempire API for this purpose. For detailed instructions on how to use Pricempire, see [Using Pricempire](PRICEMPIRE.md).

### 2. Configure Settings
Edit the `config.json` file to match your desired settings. Below is a sample configuration:

```json
{
    "empireapi": "YOUR EMPIRE API",  // Your Empire API key
    "domain": "csgoempire.tv",  // Use .com or another domain
    "price_compare_source": "steam_buy",  // Primary market source for price comparison
    "multiplier": 0.7,  // Multiplier for the primary market source
    "price_compare2": true,  // Enable a secondary market source for comparison
    "price_compare_source2": "buff",  // Secondary market source
    "multiplier2": 0.95,  // Multiplier for the secondary market source
    "price_compare_check_profitability": true,  // Enable profitability check using a different source
    "price_compare_check_profitability_source": "csgotm",  // Market source for profitability check
    "price_compare_check_profitability_source_fee": 0.9,  // Market fee for profitability check
    "price_compare_check_profitability_profit": 1.1,  // Minimum profit threshold for profitability check
    "price_range_low": 0,  // Minimum price range
    "price_range_high": 100,  // Maximum price range
    "min_liquidity": 0,  // Minimum liquidity
    "blacklist": ["Sticker | Techno4K (Holo) | Antwerp 2022", "★ StatTrak™ Karambit | Autotronic (Battle-Scarred)"],  // Blacklisted items
    "local_excel": true,  // Track bought items locally (ensure Excel is closed)
    "online_excel": false,  // Online Excel tracking (will explain later)
    "sheet_file_name": "",  // Filename for online Excel tracking
    "sheet_id": "",  // Google Sheet ID for online Excel tracking
    "bid_timer": 3.5,  // Interval in seconds between bids
    "pricempire_api":"",  // Your Pricempire API key
    "pricempire_sources":["steam_buy", "buff", "csgotm"]  // Sources you want to use; include all sources you will use
}
```

### 3. Run the Client
Once you've updated the `config.json`, run the client to start bidding.

## How It Works

Let's consider an example using `steam_buy` as the primary market source with a multiplier of `0.7`:

- Suppose the Steam Buy Order price is $100, and the item is listed on Empire for $50.
- The bot checks if `100 * 0.7 > 50`. Since this condition is true, the bot will place a bid until it is no longer profitable.

If you enable `price_compare2` and set `price_compare_source2` to `"buff"` with a multiplier of `0.95`, the bot will also check:

- If the Buff price is $66, the bot calculates `66 * 0.95 = $62.70`. It will continue to bid if this condition holds true, stopping otherwise.

For profitability checks using `csgotm` with a fee of `0.9` (representing a 10% fee) and a desired profit margin of `1.1` (10% profit):

- If the market price is $68, the bot checks `68 * 0.9 / bid price > 1.1`. If the condition fails, the bot will stop bidding.

---

## Support & Appreciation

If you find this project helpful, a +rep on my [CSGO profile](https://csgo-rep.com/profile/76561198822180159) would be greatly appreciated!

If you'd like to tip, any contribution is welcome:

- **BTC:** `bc1qc2r2up4ejy38smzjexnvqsss2wru4cry6499al`
- **ETH:** `0xCd1817B35982CEaD471951606A040ea815D5DcD0`
- **TRX (TRON):** `TENCbtD3yqPJMhwPBLcLKZQSLAyGFgV7et`
- **LTC:** `ltc1qsz0lrn9myt5sxymr8vnrwa059shqlsj3anpupg`
- **POLYGON:** `0xCd1817B35982CEaD471951606A040ea815D5DcD0`
- **BNB:** `0xCd1817B35982CEaD471951606A040ea815D5DcD0`

Thank you for your support!

---

