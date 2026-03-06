---
name: auto-install-skill
description: Automatically installs skills from GitHub when standard methods (npx skills add, git clone) fail. Fetches all skill files from raw GitHub URLs and creates them locally. Use as a fallback when cloning times out or requires authentication.
---

# Auto Install Skill

This skill automatically installs skills from GitHub repositories when standard installation methods fail. It fetches all required files from raw GitHub URLs and creates the local skill directory structure.

## When to Use This Skill

**Trigger conditions:**
- `npx skills add <package>` fails or times out (60s+ clone timeout)
- `git clone` fails with timeout, authentication required, or network error
- User requests to install a skill from a GitHub repository
- Standard installation methods are unavailable

## Automatic Fallback Workflow

```
User requests skill installation
         ↓
Try: npx skills add / git clone
         ↓
    [FAILED?]
         ↓
Auto-invoke this fallback skill
         ↓
1. Parse repo owner, repo name, skill name, branch
2. Fetch SKILL.md from raw GitHub URL
3. Scan SKILL.md for referenced files (scripts, configs)
4. Fetch each referenced file from raw GitHub URL
5. Create local skill directory
6. Write all fetched files
7. Verify and report success
```

## Input Parsing

Extract parameters from user request:

| Input Format | Extracted Values |
|--------------|------------------|
| `npx skills add https://github.com/vercel-labs/skills --skill find-skills` | owner=vercel-labs, repo=skills, skill=find-skills, branch=main |
| `Install vercel-labs/skills@find-skills` | owner=vercel-labs, repo=skills, skill=find-skills, branch=main |
| `Clone from owner/repo skill: myskill` | owner=owner, repo=repo, skill=myskill, branch=main |

**Default branch:** `main` (fallback to `master` if `main` fails)

## File Discovery Strategy

### Step 1: Fetch SKILL.md

Primary file (always required):
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/skills/{skill-name}/SKILL.md
```

### Step 2: Scan for Additional Files

Parse SKILL.md content for file references:

**Look for patterns:**
- `./script.sh`, `./bin/tool` → relative script paths
- `config.json`, `settings.yaml` → config files
- `package.json`, `requirements.txt` → dependency files
- Code blocks with file paths: `` `./myscript.py` ``
- Markdown links: `[script](./script.sh)`

**Common additional files:**
```
SKILL.md          ← Always required
script.sh         ← Shell scripts
script.py         ← Python scripts
config.json       ← Configuration
package.json      ← Node.js dependencies
requirements.txt  ← Python dependencies
README.md         ← Documentation
index.js          ← JavaScript entry point
```

### Step 3: Fetch Each File

For each discovered file, fetch from raw URL:
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/skills/{skill-name}/{filename}
```

### Step 4: Handle Missing Files

If a referenced file returns 404:
- Log warning but continue
- File may be optional or generated at runtime
- Report in final summary

## Installation Process

### Create Directory Structure

```bash
mkdir -p /root/.openclaw/workspace/skills/{skill-name}
```

### Write Files

For each fetched file:
```
Path: /root/.openclaw/workspace/skills/{skill-name}/{filename}
Content: <fetched content>
```

### Verify Installation

```bash
# Check SKILL.md exists
test -f /root/.openclaw/workspace/skills/{skill-name}/SKILL.md

# List all files
ls -la /root/.openclaw/workspace/skills/{skill-name}/
```

### Report Results

```
✅ Skill installed successfully!

Skill: {skill-name}
Source: github.com/{owner}/{repo}
Location: /root/.openclaw/workspace/skills/{skill-name}/

Files created:
  ✓ SKILL.md (4.5 KB)
  ✓ script.sh (1.2 KB)
  ✓ config.json (0.3 KB)
  ⚠ README.md (not found - may be optional)

Note: Restart Gateway to load the new skill:
  openclaw gateway restart
```

## Example Execution

### User Request
```
Install this skill: npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

### Clone Fails
```
✖ Clone timed out after 60s
```

### Auto-Fallback Executes

```bash
# 1. Parse input
owner=vercel-labs, repo=skills, skill=find-skills, branch=main

# 2. Fetch SKILL.md
web_fetch --url "https://raw.githubusercontent.com/vercel-labs/skills/main/skills/find-skills/SKILL.md"

# 3. Scan for additional files
# Result: No additional files referenced (SKILL.md is self-contained)

# 4. Create directory
mkdir -p /root/.openclaw/workspace/skills/find-skills

# 5. Write file
write --path "/root/.openclaw/workspace/skills/find-skills/SKILL.md" --content "<fetched>"

# 6. Verify
ls -la /root/.openclaw/workspace/skills/find-skills/

# 7. Report
✅ find-skills installed successfully!
```

## Error Handling

### SKILL.md Not Found

```
❌ Failed to fetch SKILL.md

Tried:
  https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill}/SKILL.md
  https://raw.githubusercontent.com/{owner}/{repo}/master/skills/{skill}/SKILL.md

Possible issues:
1. Repository doesn't exist or is private
2. Skill name is incorrect
3. Directory structure is different (e.g., src/skills/ instead of skills/)

Ask user to verify the repository URL and skill name.
```

### Network Errors

```
⚠ Network error fetching {filename}
Retrying... (attempt 2/3)
```

### Partial Installation

```
⚠ Installed with some files missing

✓ SKILL.md
✓ script.sh
✗ config.json (404 - file not found)

The skill may still work, but some features could be unavailable.
```

## Advanced Features

### Alternative Directory Structures

If standard path fails, try alternatives:

```
skills/{skill-name}/           ← Default
src/skills/{skill-name}/       ← Source subdirectory
packages/{skill-name}/         ← Package subdirectory
{skill-name}/                  ← Root level
```

### Batch Installation

For skills with many files, fetch in parallel when possible:

```bash
# Parallel fetch (conceptual)
fetch_all([
  "SKILL.md",
  "script.sh",
  "config.json",
  "package.json"
])
```

### Integrity Check

After installation, verify SKILL.md has valid YAML frontmatter:

```bash
# Check for required fields
grep -q "^name:" SKILL.md
grep -q "^description:" SKILL.md
```

## Configuration

### Default Paths

| Setting | Default |
|---------|---------|
| Skills directory | `/root/.openclaw/workspace/skills/` |
| Default branch | `main` |
| Fallback branch | `master` |
| Max retry attempts | 3 |
| Fetch timeout | 30s per file |

### Environment Overrides

```bash
export OPENCLAW_SKILLS_DIR="/custom/path/skills"
export GITHUB_DEFAULT_BRANCH="develop"
```

## Quick Reference

| Task | Command/URL |
|------|-------------|
| Raw GitHub URL | `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/skills/{skill}/{file}` |
| Create skill dir | `mkdir -p /root/.openclaw/workspace/skills/{skill}` |
| List skills | `openclaw skills list` |
| Check skill | `openclaw skills info {skill}` |
| Restart Gateway | `openclaw gateway restart` |

## Related Skills

- **clawhub**: Official skill registry CLI
- **skill-creator**: Create new skills from scratch
- **find-skills**: Search for available skills

---

**Auto-Trigger:** This skill should automatically activate when standard skill installation fails. No manual invocation needed.
