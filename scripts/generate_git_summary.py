#!/usr/bin/env python3
"""
Generate Git Summary for MkDocs

This script generates a markdown file with git repository information
including branches, recent commits, and contributors.
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path


def run_git_command(command):
    """Run a git command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {command}")
        print(f"Error: {e.stderr}")
        return ""


def get_current_branch():
    """Get current git branch"""
    return run_git_command("git rev-parse --abbrev-ref HEAD")


def get_current_commit():
    """Get current commit hash and message"""
    commit_hash = run_git_command("git rev-parse HEAD")
    commit_short = run_git_command("git rev-parse --short HEAD")
    commit_message = run_git_command("git log -1 --pretty=format:'%s'")
    commit_author = run_git_command("git log -1 --pretty=format:'%an'")
    commit_date = run_git_command("git log -1 --pretty=format:'%ci'")
    
    return {
        "hash": commit_hash,
        "short": commit_short,
        "message": commit_message,
        "author": commit_author,
        "date": commit_date
    }


def get_recent_commits(count=10):
    """Get recent commits"""
    commits = []
    git_log = run_git_command(f"git log --oneline -n {count} --pretty=format:'%h|%s|%an|%ci'")
    
    for line in git_log.split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0],
                    "message": parts[1],
                    "author": parts[2],
                    "date": parts[3]
                })
    
    return commits


def get_branches():
    """Get all branches"""
    branches = []
    
    # Local branches
    local_branches = run_git_command("git branch --format='%(refname:short)|%(objectname:short)|%(committerdate:short)'")
    for line in local_branches.split('\n'):
        if line and not line.startswith('*'):
            parts = line.split('|')
            if len(parts) == 3:
                branches.append({
                    "name": parts[0].strip(),
                    "commit": parts[1],
                    "date": parts[2],
                    "type": "local"
                })
    
    # Remote branches
    remote_branches = run_git_command("git branch -r --format='%(refname:short)|%(objectname:short)|%(committerdate:short)'")
    for line in remote_branches.split('\n'):
        if line and 'origin/HEAD' not in line:
            parts = line.split('|')
            if len(parts) == 3:
                branch_name = parts[0].strip().replace('origin/', '')
                # Avoid duplicates
                if not any(b['name'] == branch_name for b in branches):
                    branches.append({
                        "name": branch_name,
                        "commit": parts[1],
                        "date": parts[2],
                        "type": "remote"
                    })
    
    return branches


def get_contributors():
    """Get repository contributors"""
    contributors = []
    git_shortlog = run_git_command("git shortlog -sn --all")
    
    for line in git_shortlog.split('\n'):
        if line:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                contributors.append({
                    "commits": int(parts[0]),
                    "name": parts[1]
                })
    
    return contributors


def get_repository_stats():
    """Get repository statistics"""
    total_commits = run_git_command("git rev-list --all --count")
    total_files = run_git_command("git ls-files | wc -l")
    repo_size = run_git_command("git count-objects -vH | grep 'size-pack' | awk '{print $2 $3}'")
    
    first_commit_date = run_git_command("git log --reverse --format='%ci' | head -1")
    last_commit_date = run_git_command("git log -1 --format='%ci'")
    
    return {
        "total_commits": total_commits,
        "total_files": total_files.strip(),
        "repository_size": repo_size if repo_size else "N/A",
        "first_commit": first_commit_date,
        "last_commit": last_commit_date
    }


def generate_git_summary():
    """Generate the complete git summary markdown"""
    current_branch = get_current_branch()
    current_commit = get_current_commit()
    recent_commits = get_recent_commits(15)
    branches = get_branches()
    contributors = get_contributors()
    repo_stats = get_repository_stats()
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    markdown_content = f"""# Git Repository Summary

*Generated on: {timestamp}*

## Current Status

### Active Branch
- **Branch**: `{current_branch}`
- **Latest Commit**: `{current_commit['short']}`
- **Message**: {current_commit['message']}
- **Author**: {current_commit['author']}
- **Date**: {current_commit['date']}

### Repository Statistics
- **Total Commits**: {repo_stats['total_commits']}
- **Total Files**: {repo_stats['total_files']}
- **Repository Size**: {repo_stats['repository_size']}
- **First Commit**: {repo_stats['first_commit']}
- **Last Commit**: {repo_stats['last_commit']}

## Recent Commits

| Hash | Message | Author | Date |
|------|---------|--------|------|"""

    for commit in recent_commits:
        markdown_content += f"\n| `{commit['hash']}` | {commit['message']} | {commit['author']} | {commit['date'][:10]} |"

    markdown_content += f"""

## Branches

### All Branches ({len(branches)} total)

| Branch | Latest Commit | Last Updated | Type |
|--------|---------------|--------------|------|"""

    for branch in sorted(branches, key=lambda x: x['date'], reverse=True):
        branch_icon = "🌿" if branch['type'] == "local" else "🌐"
        markdown_content += f"\n| {branch_icon} `{branch['name']}` | `{branch['commit']}` | {branch['date']} | {branch['type']} |"

    markdown_content += f"""

## Contributors

### Top Contributors ({len(contributors)} total)

| Contributor | Commits | Percentage |
|-------------|---------|------------|"""

    total_commits_by_contributors = sum(c['commits'] for c in contributors)
    for contributor in contributors[:10]:  # Top 10 contributors
        percentage = (contributor['commits'] / total_commits_by_contributors * 100) if total_commits_by_contributors > 0 else 0
        markdown_content += f"\n| {contributor['name']} | {contributor['commits']} | {percentage:.1f}% |"

    markdown_content += """

## Branch Activity

```mermaid
gitgraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature work"
    checkout main
    merge develop
    commit id: "Release"
```

## Commit Activity Overview

This page provides a comprehensive overview of the repository's git history, including:

- **Current Status**: Information about the active branch and latest commit
- **Recent Commits**: The 15 most recent commits across all branches
- **Branch Overview**: All local and remote branches with their latest commits
- **Contributors**: Statistics about repository contributors and their contributions
- **Repository Statistics**: Overall repository metrics and timeline

### How This Page is Generated

This summary is automatically generated using git commands and can be refreshed by running:

```bash
python scripts/generate_git_summary.py
```

The page includes information from:
- `git log` - For commit history and messages
- `git branch` - For branch information
- `git shortlog` - For contributor statistics
- `git count-objects` - For repository size and statistics

### Key Metrics

- **Development Activity**: Track recent commits and active branches
- **Collaboration**: See contributor activity and participation
- **Repository Health**: Monitor repository growth and maintenance
- **Branch Management**: Overview of feature branches and releases

---

*This summary reflects the state of the repository at the time of generation. For real-time information, use git commands directly or regenerate this page.*
"""

    return markdown_content


def main():
    """Main function to generate and save git summary"""
    try:
        # Generate the summary
        summary_content = generate_git_summary()
        
        # Save to docs directory
        docs_path = Path(__file__).parent.parent / "docs"
        output_file = docs_path / "git-summary.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"Git summary generated successfully: {output_file}")
        
    except Exception as e:
        print(f"Error generating git summary: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
