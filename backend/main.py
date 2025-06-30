from backend.app_processes import AppProcesses

if __name__ == '__main__':
    app = AppProcesses(db_name="mgspy")
    app.process_app()

    #Only once already done
    # app.scrap_and_save_profile_data()
