
---

### 1. Login

- Visit [Pricempire](https://pricempire.com/?r=76561199570079350) and sign in using your Steam account.

### 2. Purchase a Subscription

- Go to the [subscription page](https://pricempire.com/subscribe) or navigate there through your profile.
- Choose and purchase the **Developer** or **Enterprise** plan. The **Developer** plan is sufficient for this purpose.

### 3. Obtain Your API Key

- Visit the [API page](https://pricempire.com/user/api) or access it via your profile.
- Copy your API key and paste it into the `config.json` file under the `"pricempire_api"` field.
- If necessary, whitelist your IP address by searching "what is my IP address" on Google and adding it to the API settings.

### 4. Refresh Prices

- After updating the `config.json` file with your API key and the necessary marketplace sources, run the `pricempire_prices_refresh.py` script to fetch the latest `prices.json`.

---
