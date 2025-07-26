# Email and SMS Setup Guide

## Gmail Email Configuration

Google has changed their authentication methods. Here are the current options:

### Option 1: Gmail OAuth 2.0 (Recommended)

This is the most secure and modern approach for Gmail authentication.

#### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it

#### Step 2: Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Download the JSON file containing your credentials

#### Step 3: Generate Refresh Token
1. Install the required Python packages:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2
   ```

2. Create a script to generate the refresh token:
   ```python
   from google_auth_oauthlib.flow import InstalledAppFlow
   from google.auth.transport.requests import Request
   import pickle
   import os

   # Gmail API scopes
   SCOPES = ['https://www.googleapis.com/auth/gmail.send']

   def get_gmail_credentials():
       creds = None
       
       # Load existing credentials
       if os.path.exists('token.pickle'):
           with open('token.pickle', 'rb') as token:
               creds = pickle.load(token)
       
       # If no valid credentials available, let the user log in
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file(
                   'path/to/your/credentials.json', SCOPES)
               creds = flow.run_local_server(port=0)
           
           # Save the credentials for the next run
           with open('token.pickle', 'wb') as token:
               pickle.dump(creds, token)
       
       return creds

   if __name__ == '__main__':
       creds = get_gmail_credentials()
       print(f"Refresh Token: {creds.refresh_token}")
   ```

3. Run the script and copy the refresh token

#### Step 4: Configure Environment Variables
Add these to your `.env` file:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_OAUTH2_CLIENT_ID=your-oauth2-client-id
MAIL_OAUTH2_CLIENT_SECRET=your-oauth2-client-secret
MAIL_OAUTH2_REFRESH_TOKEN=your-oauth2-refresh-token
```

### Option 2: App Passwords (If Available)

If you still have access to app passwords:

1. Go to your Google Account settings
2. Navigate to Security > 2-Step Verification
3. Look for "App passwords" (if available)
4. Generate an app password for your application
5. Use this password in your `MAIL_PASSWORD` environment variable

### Option 3: Less Secure App Access (Not Recommended)

⚠️ **Warning**: This method is being phased out by Google and is not secure.

1. Go to your Google Account settings
2. Navigate to Security
3. Turn on "Less secure app access"
4. Use your regular Gmail password

## Alternative Email Services

If Gmail authentication is problematic, consider these alternatives:

### 1. SendGrid
```bash
pip install sendgrid
```

Environment variables:
```
SENDGRID_API_KEY=your-sendgrid-api-key
MAIL_FROM=your-verified-sender@yourdomain.com
```

### 2. Mailgun
```bash
pip install requests
```

Environment variables:
```
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
MAIL_FROM=your-verified-sender@yourdomain.com
```

### 3. AWS SES
```bash
pip install boto3
```

Environment variables:
```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
MAIL_FROM=your-verified-sender@yourdomain.com
```

## SMS Configuration (Twilio)

### Step 1: Create Twilio Account
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token from the dashboard
3. Purchase a phone number

### Step 2: Configure Environment Variables
```
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

## Testing Your Configuration

Create a test script to verify your email and SMS setup:

```python
import asyncio
from notifications import NotificationService

async def test_notifications():
    service = NotificationService()
    
    # Test email
    try:
        await service.send_email_notification(
            "test@example.com",
            "Test User",
            {
                "title": "Test Notice",
                "type": "Test",
                "description": "This is a test notice",
                "post_date": "2024-01-01"
            }
        )
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Email failed: {e}")
    
    # Test SMS
    try:
        service.send_sms_notification(
            "+1234567890",
            "Test User",
            {
                "title": "Test Notice",
                "type": "Test",
                "description": "This is a test notice"
            }
        )
        print("✅ SMS sent successfully")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_notifications())
```

## Troubleshooting

### Common Email Issues:
1. **Authentication Error**: Check your credentials and authentication method
2. **Rate Limiting**: Gmail has daily sending limits
3. **Spam Filters**: Ensure your email content follows best practices

### Common SMS Issues:
1. **Invalid Phone Number**: Ensure numbers are in E.164 format (+1234567890)
2. **Account Balance**: Check your Twilio account balance
3. **Phone Number Verification**: Ensure your Twilio number is verified

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables for all sensitive data**
3. **Rotate credentials regularly**
4. **Use OAuth 2.0 when possible**
5. **Monitor your usage and costs** 