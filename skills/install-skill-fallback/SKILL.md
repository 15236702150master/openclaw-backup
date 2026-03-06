---
name: install-skill-fallback
description: Fallback skill for installing skills when git clone fails. Fetches skill files from GitHub raw URLs and creates them locally. Use when `npx skills add` or `git clone` fails during skill installation.
---

# Install Skill Fallback

This skill provides a fallback method for installing skills when the standard `npx skills add` or `git clone` commands fail (e.g., due to network timeouts, authentication issues, or private repos).

## When to Use This Skill

- `npx skills add <package>` fails or times out
- `git clone` fails (timeout, auth required, network issues)
- User explicitly asks to install a skill from GitHub
- Standard installation methods are unavailable

## How It Works

Instead of cloning the entire repository, this skill:

1. **Fetches the SKILL.md** from the GitHub raw URL
2. **Parses the skill structure** to find any additional files (scripts, configs, etc.)
3. **Fetches each required file** individually
4. **Creates the local skill directory** with all files

## Step-by-Step Process

### Step 1: Parse the Skill Source

Extract the GitHub repo and skill name from the user's request:

```
Input: "Install vercel-labs/skills --skill find-skills"
→ Repo: vercel-labs/skills
→ Skill: find-skills
→ Branch: main (default)
```

### Step 2: Fetch SKILL.md

Use `web_fetch` to get the skill definition:

```bash
https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/SKILL.md
```

Example:
```
https://raw.githubusercontent.com/vercel-labs/skills/main/skills/find-skills/SKILL.md
```

### Step 3: Parse for Additional Files

Read the SKILL.md content and look for references to other files:
- Scripts mentioned in usage examples
- Config files referenced
- Any `./` or relative paths

Common additional files:
- `script.sh`, `script.py`, etc.
- `config.json`, `config.yaml`
- `README.md`
- `package.json` (for npm-based skills)

### Step 4: Fetch Each File

For each file found, fetch from raw URL:

```
https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/<filename>
```

### Step 5: Create Local Directory

```bash
mkdir -p /root/.openclaw/workspace/skills/<skill-name>
```

### Step 6: Write All Files

Write each fetched file to the local directory.

### Step 7: Verify and Report

Check that SKILL.md exists and report:

```
✅ Skill installed successfully!

Location: /root/.openclaw/workspace/skills/<skill-name>/
Files created:
  - SKILL.md
  - <other files...>

Note: You may need to restart the Gateway for the skill to be recognized:
  openclaw gateway restart
```

## Example Commands

### Install find-skills from vercel-labs/skills

```bash
# Fetch SKILL.md
web_fetch --url "https://raw.githubusercontent.com/vercel-labs/skills/main/skills/find-skills/SKILL.md"

# Create directory
mkdir -p /root/.openclaw/workspace/skills/find-skills

# Write the content
write --path "/root/.openclaw/workspace/skills/find-skills/SKILL.md" --content "<fetched content>"
```

### Install skill with multiple files

```bash
# Fetch all files
web_fetch --url "https://raw.githubusercontent.com/owner/repo/main/skills/myskill/SKILL.md"
web_fetch --url "https://raw.githubusercontent.com/owner/repo/main/skills/myskill/script.sh"
web_fetch --url "https://raw.githubusercontent.com/owner/repo/main/skills/myskill/config.json"

# Create directory and write all files
mkdir -p /root/.openclaw/workspace/skills/myskill
# Write each file...
```

## Error Handling

### If SKILL.md fetch fails

```
❌ Failed to fetch SKILL.md from:
   https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md

Possible reasons:
1. Repository doesn't exist or is private
2. Skill name is incorrect
3. Branch is not 'main' (try 'master' or ask user)

Ask user to verify:
- Repository URL
- Skill name
- Branch name
```

### If additional files fail

Continue with just SKILL.md if other files are optional. Report:

```
⚠️ Installed with partial files
   - SKILL.md ✓
   - script.sh ✗ (file not found, may be optional)
```

## Tips

1. **Check branch name**: Most repos use `main`, some use `master`. Try both if one fails.

2. **Verify file paths**: Some skills may have different directory structures:
   - `skills/<name>/` (most common)
   - `src/skills/<name>/`
   - `packages/<name>/`

3. **Check SKILL.md header**: The YAML frontmatter contains the skill name and description - verify it matches what the user requested.

4. **Gateway restart**: Skills are loaded at session start. After installing, remind user to restart if the skill doesn't appear immediately.

## Quick Reference

| Task | Command/URL Pattern |
|------|---------------------|
| Fetch SKILL.md | `https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md` |
| Fetch other file | `https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/<file>` |
| Create directory | `mkdir -p /root/.openclaw/workspace/skills/<skill>` |
| Verify install | `ls -la /root/.openclaw/workspace/skills/<skill>/` |
| List skills | `openclaw skills list` |
| Restart Gateway | `openclaw gateway restart` |

## Related Skills

- **clawhub**: Official skill registry CLI for browsing and installing skills
- **skill-creator**: Create or update skills manually

---

**Remember**: This is a fallback method. Always try `npx skills add` or `clawhub install` first, then use this skill if those fail.
