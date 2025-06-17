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

## 📋 **Current Workflows**

- `crewai-integration.json` - Basic CrewAI API integration workflow
- (Add your workflow files here and update this list)

## ⚠️ **Important Notes**

- **Workflows are NOT automatically backed up**
- **Docker volume deletion will lose all workflows**
- **Export manually or use backup script regularly**
- **Team members need to import workflows manually** 