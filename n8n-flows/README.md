# n8n Workflows Backup

This directory contains exported n8n workflows for version control and sharing.

## 📤 **How to Export Workflows (Manual)**

1. **Open n8n**: http://localhost:5678
2. **Go to Settings** → **Import/Export**  
3. **Select workflows** to export
4. **Download JSON file**
5. **Save to this directory** (`n8n-flows/`)
6. **Commit to git**:
   ```bash
   git add n8n-flows/
   git commit -m "feat: Add new workflow - [workflow name]"
   git push origin main
   ```

## 📥 **How to Import Workflows**

1. **Open n8n**: http://localhost:5678
2. **Go to Settings** → **Import/Export**
3. **Choose file** from this directory  
4. **Import** the workflow

## 🔄 **Automated Backup**

Run the backup script periodically:
```bash
./scripts/backup-n8n.sh
```

## 📋 **Workflow Management**

**Note**: Workflow JSON files are excluded from git (private business logic).

## 🔒 **Privacy & Local Backup**

Your workflows contain private business logic and are excluded from version control.

### **Local Backup Options**:
1. **Manual exports** to local file system outside git
2. **Use backup script** with local storage only  
3. **Private git repository** for workflows only
4. **Cloud backup** (Dropbox, Google Drive, etc.)

## ⚠️ **Important Notes**

- **Workflows are private** - not shared in public repository
- **Docker volume deletion will lose all workflows**
- **Backup locally or to private storage regularly**
- **Team sharing requires separate private repository/method** 