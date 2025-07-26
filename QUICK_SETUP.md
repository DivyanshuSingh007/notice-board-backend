# 🚀 Quick Setup Guide - Email & SMS Notifications

## ✅ What's Already Done:
- ✅ Notification dependencies installed
- ✅ Notification service created
- ✅ Backend integrated with notifications
- ✅ User has email and mobile number
- ✅ User is admin

## 📧 Email Setup (Gmail):

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → App passwords
   - Select "Mail" and your device
   - Copy the generated password

### Step 2: Create .env file
Create a `.env` file in your project root:

```env
# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com

# SMS Configuration (Twilio) - Optional
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

## 📱 SMS Setup (Twilio) - Optional:

### Step 1: Create Twilio Account
1. Go to [twilio.com](https://twilio.com)
2. Sign up for a free account
3. Get your Account SID and Auth Token from the dashboard

### Step 2: Get a Phone Number
1. In Twilio Console, go to Phone Numbers
2. Buy a phone number (free trial available)
3. Copy the phone number

## 🧪 Testing:

### Test Email Only (Recommended first):
```bash
curl -X POST "http://localhost:8000/notice/test-notifications" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Test with Real Notice:
Create a new notice through your frontend - notifications will be sent automatically.

## 📋 Current User:
- **Email:** divyanshusingh6363@gmail.com
- **Mobile:** 09219609232
- **Admin:** ✅ Yes

## 🎯 What Happens:
1. **Admin creates a notice** → Notifications sent automatically
2. **All registered users** receive email + SMS
3. **Beautiful HTML emails** with notice details
4. **Concise SMS messages** with key information

## 🔒 Security Notes:
1. **Never commit your `.env` file** to version control
2. **Use App Passwords** for Gmail (not your regular password)
3. **Keep Twilio credentials secure**

## 🚀 Next Steps:
1. Set up your email credentials in `.env`
2. Test with the test endpoint
3. Create a real notice to see notifications in action!

## 📞 Support:
If you need help, check the logs for error messages and verify your configuration. 