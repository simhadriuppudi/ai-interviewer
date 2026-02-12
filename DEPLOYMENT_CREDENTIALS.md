# AI Interviewer - Deployment Credentials

## 🔐 Production Credentials

**Generated on**: 2026-02-10

### Strong Secret Key (JWT)
```
EvCF-SmaNGsy8s3K1v2vL9r6RE5R-nQZtehT26vC4Ns
```

### Gemini API Key
```
AIzaSyB4wAyGTwPKk8coP4Vd7dge9rNXJUq0UqE
```

---

## 📋 Render Environment Variables

Copy these to Render.com when deploying:

| Variable | Value |
|----------|-------|
| `GEMINI_API_KEY` | `AIzaSyB4wAyGTwPKk8coP4Vd7dge9rNXJUq0UqE` |
| `SECRET_KEY` | `EvCF-SmaNGsy8s3K1v2vL9r6RE5R-nQZtehT26vC4Ns` |
| `DATABASE_URL` | `sqlite:///./interview.db` |
| `API_V1_STR` | `/api/v1` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` |
| `GEMINI_MODEL` | `gemini-3-flash-preview` |

---

## 🚀 Expected Deployment URL Format

After deploying to Render, your URL will be:

```
https://[your-service-name].onrender.com
```

Examples:
- `https://ai-interviewer.onrender.com`
- `https://ai-interviewer-simha.onrender.com`
- `https://my-ai-interviewer.onrender.com`

---

## ✅ Testing Your Deployment

Once deployed, test these URLs (replace with your actual URL):

1. **Homepage**: `https://your-app.onrender.com/`
2. **Health Check**: `https://your-app.onrender.com/api/v1/health`
3. **Register**: `https://your-app.onrender.com/register.html`
4. **Login**: `https://your-app.onrender.com/login.html`
5. **Dashboard**: `https://your-app.onrender.com/dashboard.html`

---

## ⚠️ Security Notes

- ✅ Strong secret key generated (32-byte URL-safe)
- ✅ Never commit `.env` file to Git (already in `.gitignore`)
- ✅ Use environment variables on Render (not hardcoded)
- ⚠️ Keep these credentials secure
- 🔄 Rotate keys if compromised

---

## 📝 Fill in After Deployment

**Your Deployment URL**: `_________________________________`

**Deployed On**: `_________________________________`

**Status**: ✅ Live / ⏸️ Sleeping / ❌ Error
