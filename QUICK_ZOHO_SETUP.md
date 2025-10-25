# Quick Setup Guide: Zoho Books OAuth 2.0

## Important: One-Time Setup (App Owner Does This Once)

The Client ID and Secret are YOUR APPLICATION's credentials (not user credentials).
You register once, then ALL users can connect with just their Zoho login.

### Step 1: Register Your Application with Zoho (5 minutes)

1. Go to: https://api-console.zoho.com/
2. Click "Add Client" → "Server-based Applications"
3. Fill in:
   - **Client Name**: Vasool Collections Platform
   - **Homepage URL**: http://localhost:3000 (or your domain)
   - **Authorized Redirect URIs**: 
     ```
     http://localhost:3000/zoho/callback
     ```
     (For production, use: https://yourdomain.com/zoho/callback)

4. Click "CREATE"

5. You'll see:
   ```
   Client ID: 1000.XXXXXXXXXXXXXXXXXXXXX
   Client Secret: xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Step 2: Add to Backend Environment Variables

Open `/app/backend/.env` and add:

```bash
# Zoho Books OAuth (App credentials - set once)
ZOHO_CLIENT_ID=1000.YOUR_CLIENT_ID_HERE
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REDIRECT_URI=http://localhost:3000/zoho/callback
```

### Step 3: Restart Backend
```bash
sudo supervisorctl restart backend
```

## That's It! Now ANY User Can Connect:

1. User clicks "Connect with Zoho Books"
2. User is redirected to Zoho's login page
3. User enters THEIR Zoho username/password
4. Zoho asks: "Allow Vasool to access your Zoho Books?"
5. User clicks "Accept"
6. OAuth tokens are automatically stored
7. ✅ Connected! Dashboard gets real data from Zoho Books

## What Happens After Connection:

✅ **Dashboard gets real data**: Outstanding invoices, payments, customer info
✅ **AI Chat with real insights**: Analytics Agent uses Zoho Books API to analyze actual data
✅ **No more DUMMY DATA labels**: Chat shows real financial insights
✅ **Automatic data sync**: Refreshes data periodically

## Testing Right Now (Without Real Zoho Account):

Use **Demo Mode** to test the full UI/UX:
- Click "Connect with Zoho Books" 
- Click "OK" for Demo Mode
- See how it works before setting up real OAuth

Once you add real Client ID/Secret, it works with actual Zoho data!
