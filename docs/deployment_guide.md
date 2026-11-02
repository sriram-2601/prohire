# Week 4 Full-Stack Deployment Guide

This guide covers deploying the **Indigo.ai / Enterprise Structured Ingestion Firewall** full-stack application to production using **Supabase**, **Render**, and **Vercel**.

---

## 1. Database Setup: Supabase (PostgreSQL)

1. Create a free project at [supabase.com](https://supabase.com).
2. Navigate to **Project Settings** → **Database** → **Connection string**.
3. Select **URI** (or Transaction Pooler / Session Pooler) and copy the connection string:
   ```text
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
   ```
4. Optional: Run `backend/sql/supabase_schema.sql` in the **SQL Editor**, or let the backend create tables automatically on its first boot.

---

## 2. Backend Deployment: Render

1. Create a free account at [render.com](https://render.com).
2. Connect your GitHub repository.
3. Click **New +** → **Web Service** (or use Blueprint with `render.yaml`).
4. Configure service settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
5. Configure Environment Variables:
   - `GROQ_API_KEY`: Your key from [console.groq.com](https://console.groq.com)
   - `GROQ_MODEL`: `llama-3.3-70b-versatile`
   - `DATABASE_URL`: Your Supabase connection string from Step 1
   - `ALLOWED_ORIGINS`: Your Vercel frontend URL (e.g., `https://your-app.vercel.app`)
6. Deploy the service and verify `https://your-service.onrender.com/health` returns:
   ```json
   {
     "status": "ok",
     "database": "postgres",
     "database_ok": true,
     "groq_api_key_configured": true
   }
   ```

---

## 3. Frontend Deployment: Vercel

1. Create an account at [vercel.com](https://vercel.com).
2. Import your GitHub repository.
3. Select **Framework Preset**: `Vite`.
4. Set **Root Directory**: `frontend-react`.
5. Configure Environment Variables:
   - `VITE_API_URL`: Your Render backend URL without trailing slash (e.g. `https://your-service.onrender.com`).
6. Click **Deploy**.

---

## 4. End-to-End Verification Checklist

- [ ] Open your deployed Vercel URL in a browser.
- [ ] Confirm the header status indicator shows "Online".
- [ ] Send a test query: *"I received the wrong item in order #12345"*.
- [ ] Verify the firewall correctly classifies intent (`order_tracking` or `payment_issue`), risk, and priority in the side panel.
- [ ] Verify the LLM response streams in formatted Markdown.
- [ ] Ask a follow-up: *"Can I get a replacement instead?"* to verify conversation memory.
- [ ] Check Supabase table editor to verify conversation and message rows are persisted in PostgreSQL.
