from src import info_filter


def vel_info_per_js(periods: list, json: str):
    info_filter.vel_info(periods, json)

if __name__ == "__main__":
    periods = [26, 28, 30, 32, 34,] # 40, 45, 50, 60, 70, 80, 90, 100, 111, 125, 135, 143]
    periods = [32]
    periods = [20, 26, 28, 30, 32, 34]

    vel_info_per_js(periods, "vel_info.json")

