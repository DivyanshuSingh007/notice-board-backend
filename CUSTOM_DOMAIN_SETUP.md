# Custom Domain Deployment Guide

This guide will help you deploy your Notice Board application using your own custom domain.

## **Domain Structure Example**

```
yourdomain.com (or notice.yourdomain.com)
├── Frontend: app.yourdomain.com
├── Backend API: api.yourdomain.com  
└── Email: notifications@yourdomain.com
```

## **Step 1: Domain DNS Configuration**

### **1.1 Access Your Domain Registrar**
- Go to your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.)
- Access DNS management

### **1.2 Add DNS Records**

#### **For Railway (Backend)**
```
Type: CNAME
Name: api
Value: [Railway-provided CNAME]
TTL: 3600
```

#### **For Vercel (Frontend)**
```
Type: A
Name: app (or @ for root domain)
Value: [Vercel-provided IP]
TTL: 3600

Type: CNAME
Name: www
Value: app.yourdomain.com
TTL: 3600
```

## **Step 2: Backend Deployment (Railway)**

### **2.1 Deploy to Railway**
1. Push your backend code to GitHub
2. Connect Railway to your GitHub repo
3. Deploy the application

### **2.2 Configure Custom Domain**
1. Go to Railway dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Click **"Add Domain"**
5. Enter: `api.yourdomain.com`
6. Railway will provide a CNAME record
7. Add this CNAME to your domain's DNS

### **2.3 Set Environment Variables**
```env
RESEND_API_KEY=re_ck1GGaik_u8gj7CPjghGub9zjidpA271R
MAIL_FROM=notifications@yourdomain.com
SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///./notice.db
```

## **Step 3: Frontend Deployment (Vercel)**

### **3.1 Deploy to Vercel**
1. Push your frontend code to GitHub
2. Connect Vercel to your GitHub repo
3. Deploy the application

### **3.2 Configure Custom Domain**
1. Go to Vercel dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Click **"Add Domain"**
5. Enter: `app.yourdomain.com`
6. Vercel will provide DNS records
7. Add these records to your domain's DNS

### **3.3 Update API Configuration**
In your frontend code, update the API base URL:
```javascript
// config.js or similar
const API_BASE_URL = 'https://api.yourdomain.com'
```

## **Step 4: Email Domain Setup (Resend)**

### **4.1 Add Domain to Resend**
1. Go to [Resend Domains](https://resend.com/domains)
2. Click **"Add Domain"**
3. Enter: `yourdomain.com`
4. Verify domain ownership

### **4.2 Configure DNS Records for Email**
Add these records to your domain's DNS:
```
Type: TXT
Name: @
Value: resend-verification=your-verification-code

Type: CNAME
Name: resend._domainkey
Value: resend._domainkey.yourdomain.com
```

### **4.3 Update Email Configuration**
Update your backend environment variables:
```env
MAIL_FROM=notifications@yourdomain.com
```

## **Step 5: SSL Certificate Setup**

### **5.1 Automatic SSL (Recommended)**
- Railway and Vercel provide automatic SSL certificates
- No additional configuration needed

### **5.2 Manual SSL (If needed)**
- Use Let's Encrypt for free SSL certificates
- Configure with your hosting provider

## **Step 6: Testing Your Setup**

### **6.1 Test Backend API**
```bash
curl https://api.yourdomain.com/docs
```

### **6.2 Test Frontend**
Visit: `https://app.yourdomain.com`

### **6.3 Test Email Notifications**
1. Create a test notice
2. Check if emails are sent from `notifications@yourdomain.com`

## **Step 7: Production Optimization**

### **7.1 Environment Variables**
```env
# Production settings
NODE_ENV=production
CORS_ORIGINS=https://app.yourdomain.com
```

### **7.2 Database Setup**
- Consider using PostgreSQL for production
- Set up database backups

### **7.3 Monitoring**
- Set up uptime monitoring
- Configure error tracking

## **Common Issues & Solutions**

### **DNS Propagation**
- DNS changes can take 24-48 hours to propagate
- Use tools like `dig` or `nslookup` to check propagation

### **SSL Certificate Issues**
- Ensure DNS is properly configured before adding custom domain
- Wait for SSL certificate generation (can take up to 24 hours)

### **Email Delivery**
- Verify domain in Resend dashboard
- Check SPF and DKIM records
- Test email delivery with different providers

## **Cost Breakdown**

### **Domain Registration**
- Domain: $10-15/year
- DNS hosting: Usually free with registrar

### **Hosting**
- Railway: Free tier available
- Vercel: Free tier available
- Email (Resend): 3,000 emails/month free

### **Total Estimated Cost**
- **Free tier**: $10-15/year (domain only)
- **Paid tier**: $20-50/month (depending on usage)

## **Next Steps**

1. **Choose your domain name**
2. **Set up DNS records**
3. **Deploy backend to Railway**
4. **Deploy frontend to Vercel**
5. **Configure email domain**
6. **Test all functionality**

Your Notice Board app will be live at:
- **Frontend**: `https://app.yourdomain.com`
- **API**: `https://api.yourdomain.com`
- **Email**: `notifications@yourdomain.com` 