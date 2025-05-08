import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config("api.app:app", host="0.0.0.0", port=3600, reload=True,  reload_dirs=["app", "shared_libs"])
    server = uvicorn.Server(config)
    server.run()

