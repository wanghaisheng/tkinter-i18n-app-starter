# tkinter-i18n-app-starter

python version >3.10 




if we use subprocess to  start fastapi server, when freeze with pyinstaller or cx freeze  ,it will bring you all kinds of module not found issues


so .



    app.mount("/static", StaticFiles(directory=os.path.join(tmp["ROOT_DIR"],"static")), name="static")

    config = uvicorn.Config(app, loop=loop, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    try:
        loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        print("Received Ctrl+C. Stopping gracefully...")
        # Cancel all running tasks
        for task in asyncio.Task.all_tasks():
            task.cancel()
