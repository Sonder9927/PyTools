from src import info_filter


def vel_info_per_js(periods: list, json: str):
    info_filter.vel_info(periods, json, .5)

if __name__ == "__main__":
    periods = [20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
    periods = [20, 26, 28, 30, 34]
    periods = [20]

    vel_info_per_js(periods, "vel_info.json")

