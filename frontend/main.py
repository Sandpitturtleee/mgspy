from datetime import datetime

from frontend.data_collectors import DataCollectors

if __name__ == '__main__':
    collector = DataCollectors()

    start_dt = datetime(2025, 6, 28, 11, 0, 0)
    end_dt = datetime(2025, 6, 28, 12, 0, 0)
    timestamps = collector.get_player_activity(nick="Luxvyu", start_dt=start_dt, end_dt=end_dt)
    collector.plot_player_activity(timestamps=timestamps, start_dt=start_dt, end_dt=end_dt)