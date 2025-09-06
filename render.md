
## 1. Docker
##### Root Directory(Optional)

*Desc:* If set, Render runs commands from this directory instead of the repository root. Additionally, code changes outside of this directory do not trigger an auto-deploy. Most commonly used with a [monorepo.](https://render.com/docs/monorepo-support#root-directory)
[input]
##### Dockerfile Path

**Desc:** The path to your service's Dockerfile, relative to the repo root. Defaults to `./Dockerfile`.

[input]

## 2. Web Service 
##### Root Directory (Optional)

**Desc:** If set, Render runs commands from this directory instead of the repository root. Additionally, code changes outside of this directory do not trigger an auto-deploy. Most commonly used with a [monorepo](https://render.com/docs/monorepo-support#root-directory)
[input]
##### Build Command

**Desc:** Render runs this command to build your app before each deploy.

[input]

##### Start Command

**Desc:** Render runs this command to start your app with each deploy.

[input]

If app is docker use 1 else use number 2 path