from fastapi import FastAPI

from api.routers import auth, posts, ratings, users

app = FastAPI(title="Social Network API", version="2.0")

for module in (auth, users, posts, ratings):
    app.include_router(module.router)
