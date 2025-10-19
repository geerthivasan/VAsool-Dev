# Zoho Books OAuth 2.0 Integration Setup

## Overview
This application integrates with Zoho Books using OAuth 2.0 for secure access to accounting data. The implementation follows Zoho's official OAuth 2.0 API documentation.

## Two Connection Modes

### 1. Demo Mode (No Setup Required)
- Click "OK" when prompted during connection
- Perfect for testing and development
- Simulates Zoho Books connection
- Shows all UI features without real data

### 2. Production Mode (Requires Zoho OAuth App)
To enable real Zoho Books OAuth integration:

## Step-by-Step Setup for Production

### 1. Create Zoho OAuth Client
1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Click "Add Client" → "Server-based Applications"
3. Fill in the details:
   - **Client Name**: Vasool Collections Platform (or your app name)
   - **Homepage URL**: Your application's homepage URL
   - **Authorized Redirect URIs**: 
     ```
     http://localhost:3000/zoho/callback  (for local development)
     https://yourdomain.com/zoho/callback  (for production)
     ```

### 2. Get Your Credentials
After creating the client, you'll receive:
- **Client ID**: e.g., `1000.XXXXXXXXXXXXXXXXXXXXXXX`
- **Client Secret**: e.g., `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 3. Configure Environment Variables

Add these to your `/app/backend/.env` file:

```bash
# Zoho Books OAuth Configuration
ZOHO_CLIENT_ID=1000.YOUR_CLIENT_ID_HERE
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REDIRECT_URI=http://localhost:3000/zoho/callback

# For production deployment, use your production URL:
# ZOHO_REDIRECT_URI=https://yourdomain.com/zoho/callback
```

### 4. Update Frontend Environment (if needed)

The frontend uses `REACT_APP_BACKEND_URL` which is already configured. The callback URL is automatically constructed.

### 5. Restart Backend
```bash
sudo supervisorctl restart backend
```

## OAuth Flow

1. **User clicks "Connect with Zoho Books"**
2. **Select Production Mode** (click Cancel on the prompt)
3. **Redirect to Zoho Login Page** - User logs in with their Zoho credentials
4. **User Authorizes Access** - Grants permissions to read Zoho Books data
5. **Zoho Redirects Back** - With authorization code
6. **Backend Exchanges Code** - For access token and refresh token
7. **Tokens Stored Securely** - In encrypted format (production)
8. **Connection Complete** - User can now use integrated features

## Scopes Requested

```
ZohoBooks.fullaccess.all
```

This scope allows the application to:
- Read invoices and outstanding payments
- Access customer payment history
- View financial reports
- Track payment patterns

## Security Features

✅ **OAuth 2.0 Standard** - Industry-standard security protocol
✅ **State Token** - CSRF protection
✅ **Encrypted Storage** - Tokens stored securely (production)
✅ **Refresh Token** - Long-lived, automatic token refresh
✅ **User Revocable** - Users can revoke access anytime from Zoho

## Testing the Integration

### Demo Mode (Default)
```bash
1. Login to application
2. Click "Connect" button
3. Select "Zoho Books"
4. Click "Connect with Zoho Books"
5. Click "OK" for Demo Mode
6. ✅ Connection successful!
```

### Production Mode (With Real Credentials)
```bash
1. Set up Zoho OAuth app (steps above)
2. Configure environment variables
3. Restart backend
4. Login to application
5. Click "Connect" → "Zoho Books"
6. Click "Connect with Zoho Books"
7. Click "Cancel" for Production OAuth
8. Login to Zoho when redirected
9. Authorize access
10. ✅ Redirected back with real connection!
```

## Troubleshooting

### "Zoho Books refused to connect"
- **Cause**: Demo OAuth credentials being used
- **Solution**: Either use Demo Mode OR set up real OAuth credentials

### "Invalid redirect URI"
- **Cause**: Redirect URI mismatch between Zoho console and application
- **Solution**: Ensure `ZOHO_REDIRECT_URI` matches exactly what's configured in Zoho API Console

### "Invalid state token"
- **Cause**: CSRF token mismatch or expired
- **Solution**: Try connecting again, state tokens are single-use

### "Token exchange failed"
- **Cause**: Invalid client credentials
- **Solution**: Verify `ZOHO_CLIENT_ID` and `ZOHO_CLIENT_SECRET` are correct

## API Documentation

For more details, refer to:
- [Zoho Books API - OAuth](https://www.zoho.com/books/api/v3/oauth/)
- [Zoho OAuth 2.0 Guide](https://www.zoho.com/accounts/protocol/oauth/web-server-applications.html)

## Support

For issues with Zoho OAuth setup:
1. Check Zoho API Console logs
2. Verify environment variables
3. Check backend logs: `tail -f /var/log/supervisor/backend.err.log`
4. Test with Demo Mode first to isolate OAuth issues
