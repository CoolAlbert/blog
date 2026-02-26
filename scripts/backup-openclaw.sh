#!/bin/bash
# Daily full backup of .openclaw directory
# Runs at 22:00 Moscow time

BACKUP_DIR="/home/user/openclaw_backups"
BACKUP_FILE="openclaw-full-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

# Create backups directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create compressed archive of entire .openclaw directory
# No exclusions needed - backups are stored outside .openclaw
tar -czf "$BACKUP_DIR/$BACKUP_FILE" -C /home/user .openclaw

echo "Backup created: $BACKUP_DIR/$BACKUP_FILE"
echo "Size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "openclaw-backup-*.tar.gz" -type f -mtime +7 -delete

echo "Old backups cleaned (keeping last 7 days)"
echo "$BACKUP_DIR/$BACKUP_FILE"
