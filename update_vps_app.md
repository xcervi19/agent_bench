# SSH into the VPS
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212

# Inside the VPS, navigate to the project
cd ~/agent_bench

# Pull the latest code
git pull origin main  # or whatever your branch is

# Rebuild the claude_agent image
docker compose build claude_agent

# Restart the service
docker compose up -d claude_agent

# Verify it's running
docker compose logs -f claude_agent