#!/bin/bash
# De Luca Social — GitHub deploy script
# Run once from this folder: bash deploy.sh

TOKEN="REDACTED"
USERNAME="s7612f"
REPO="deluca-social"

echo "Creating GitHub repo..."
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO\",\"description\":\"De Luca Cucina social media content hub\",\"private\":false,\"auto_init\":false}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Repo created:', d.get('html_url','error: '+str(d)))"

sleep 2

echo "Initialising git..."
git init
git add .
git commit -m "Initial commit — De Luca content hub"
git branch -M main
git remote add origin https://$USERNAME:$TOKEN@github.com/$USERNAME/$REPO.git
git push -u origin main

echo "Enabling GitHub Pages..."
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$USERNAME/$REPO/pages \
  -d '{"source":{"branch":"main","path":"/site"}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Pages:', d.get('html_url','Enabling... check github.com/'+\"$USERNAME\"+\"/\"+\"$REPO\"+\"/settings/pages\"))"

echo ""
echo "Done! Site will be live in ~60 seconds at:"
echo "https://$USERNAME.github.io/$REPO"
