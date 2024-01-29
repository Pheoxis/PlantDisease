# PlantDisease

## Docker instruction

Install docker if you do not have it already.

The instruction:

1. Go to main directory;
2. Run: `docker compose up`, if you changed your code you should rebuild the image, run `docker compose up --build`; 
3. On `127.0.0.1:80` the `frontend` will be listening, on `127.0.0.1:8000` the `backend` will be listening;
4. Press Ctrl+C to turn down containers;
5. Remeber to run `docker prune` once in a while.
6. In repositury under DataBase you can find .JPG to run code on them. If you want to try some of yours .JPG make sure they are 256x256 and its a photo of tomatoe leaf.
