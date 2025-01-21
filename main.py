from website import create_app


app = create_app()

# Runs the app (Website)
if __name__ == '__main__':
    app.run()