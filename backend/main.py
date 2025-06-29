from backend.app_processes import AppProcesses

if __name__ == '__main__':
    app = AppProcesses(db_name="mgspy")
    app.process_app()
