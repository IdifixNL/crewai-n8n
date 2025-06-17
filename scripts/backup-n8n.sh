#!/bin/bash

# Backup n8n workflows to git repository
# Run this script periodically to keep workflows backed up

echo "🔄 Backing up n8n workflows..."

# Create flows directory if it doesn't exist
mkdir -p n8n-flows

# Export n8n data from Docker volume
docker run --rm \
  -v crewai_n8n_automation_n8n_data:/data \
  -v $(pwd)/n8n-flows:/backup \
  alpine:latest \
  sh -c "cp -r /data/workflows /backup/ 2>/dev/null || echo 'No workflows found'"

# If workflows exist, commit them
if [ -d "n8n-flows/workflows" ]; then
  echo "✅ Workflows found - adding to git"
  git add n8n-flows/
  git commit -m "backup: Update n8n workflows" || echo "No changes to commit"
  git push origin main
  echo "🎉 n8n workflows backed up successfully!"
else
  echo "ℹ️ No workflows found to backup"
fi 