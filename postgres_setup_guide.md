# PostgreSQL Migration Guide - Departmental ERP System

## 🚀 पूर्ण गाईड: SQLite ते PostgreSQL मायग्रेशन

### 📋 आवश्यक शक्त्या:

1. **PostgreSQL सर्व्हर** (इनस्टॉल केलेला)
2. **pgAdmin** (डेटाबेस बघण्यासाठी)
3. **Python psycopg2-binary** लायब्ररी

---

## 🛠️ स्टेप १: PostgreSQL सेटअप

### 1. PostgreSQL इनस्टॉल करा:
```bash
# Windows वरील डाउनलोड लिंक:
# https://www.postgresql.org/download/windows/

# इनस्टॉलेशन दरम्यान:
# - Password: admin (किंवा तुमचा पसंतीचा)
# - Port: 5432 (default)
# - Include pgAdmin 4
```

### 2. pgAdmin मध्ये लॉगिन करा:
- **Username:** postgres
- **Password:** admin (तुम्ही सेट केलेला)
- **Port:** 5432

---

## 🔄 स्टेप २: मायग्रेशन चालवा

### 1. Python डिपेंडन्सी इनस्टॉल करा:
```bash
pip install psycopg2-binary
```

### 2. मायग्रेशन स्क्रिप्ट चालवा:
```bash
python migrate_to_postgresql.py
```

### 3. मायग्रेशन काय करते:
- ✅ PostgreSQL मध्ये `departmental_erp` डेटाबेस तयार करते
- ✅ सर्व 22 टेबल्स तयार करते
- ✅ SQLite मधील डेटा PostgreSQL मध्ये मूव्ह करते
- ✅ Application configuration अपडेट करते

---

## 📊 स्टेप ३: pgAdmin मध्ये डेटाबेस बघा

### 1. pgAdmin उघडा
### 2. **Servers** → **PostgreSQL** → **Databases** → **departmental_erp**
### 3. **Schemas** → **public** → **Tables**

### मुख्य टेबल्स तुम्हाला दिसतील:
- 🗂️ **user** - सर्व वापरकर्ते
- 🗂️ **subject** - विषय माहिती
- 🗂️ **complaint** - तक्रारी
- 🗂️ **workload** - फॅकल्टी वर्कलोड
- 🗂️ **marks** - विद्यार्थी गुण
- आणि इतर 17 टेबल्स...

---

## ⚙️ कॉन्फिगरेशन डिटेल्स

### Database Connection Details:
- **Host:** localhost
- **Port:** 5432
- **Database:** departmental_erp
- **Username:** postgres
- **Password:** admin

### Updated Configuration Files:
- `config.py` - PostgreSQL connection string
- `app.py` - Database URI updated

---

## 🧪 स्टेप ४: टेस्टिंग

### 1. अ‍ॅप्लिकेशन चालवा:
```bash
python app.py
```

### 2. ब्राउजर मध्ये उघडा:
```
http://localhost:5000
```

### 3. लॉगिन टेस्ट करा:
- **HOD:** username: `hoduser`, password: `hodpass`
- **CC:** username: `ccuser`, password: `ccpass`
- **Faculty:** username: `facultyuser`, password: `facultypass`
- **Student:** username: `studentuser`, password: `studentpass`

---

## 🔍 स्टेप ५: pgAdmin मध्ये डेटा तपासा

### SQL Queries for Verification:

```sql
-- सर्व वापरकर्ते पहा
SELECT * FROM "user";

-- विषय पहा
SELECT * FROM subject;

-- तक्रारी पहा
SELECT * FROM complaint;

-- वर्कलोड पहा
SELECT * FROM workload;

-- टेबल संख्या पहा
SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';
```

---

## 📱 मोबाईल अ‍ॅप्लिकेशनसाठी

### PostgreSQL मोबाईल कनेक्शन:
```python
# मोबाईल अ‍ॅपसाठी connection string
DATABASE_URL = "postgresql://postgres:admin@YOUR_IP:5432/departmental_erp"
```

---

## 🚨 ट्रबलशूटिंग

### Common Issues:

1. **Connection Failed:**
   - PostgreSQL service चालू आहे का?
   - Password बरोबर आहे का?

2. **Permission Denied:**
   ```sql
   -- pgAdmin मध्ये run करा
   ALTER USER postgres CREATEDB;
   ```

3. **Port Already in Use:**
   - Task Manager मध्ये PostgreSQL process check करा
   - Port change करा (5432 वरून 5433)

---

## 📈 परफॉर्मन्स बेनिफिट्स

### PostgreSQL vs SQLite:
- ✅ **Multi-user support** - एकाच वेळी 100+ वापरकर्ते
- ✅ **Better security** - Role-based access control
- ✅ **Scalability** - TB डेटा सपोर्ट
- ✅ **Backup & Recovery** - Automated backups
- ✅ **Remote access** - मोबाईल/वेब अ‍ॅप्स

---

## 🎯 नेक्स्ट स्टेप्स

1. **Backup Strategy:** Daily automated backups सेट करा
2. **Monitoring:** pgAdmin मध्ये performance monitoring
3. **Security:** Strong passwords आणि SSL connections
4. **Integration:** मोबाईल अ‍ॅप्ससाठी API endpoints

---

## 📞 हेल्प आणि सपोर्ट

### मायग्रेशन अयशस्वी झाल्यास:
1. PostgreSQL logs तपासा
2. Migration script error messages वाचा
3. pgAdmin मध्ये manual table creation करू शकता

### Contact Support:
- Database Administrator
- PostgreSQL Documentation
- Stack Overflow

---

**🎉 Congratulations!** तुमचा Departmental ERP System आता PostgreSQL वर चालू आहे!
