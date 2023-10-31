from src.plot_results import Painter


def main():
    pr = Painter(init=True)
    # pr.area("model")
    pr.phase("tpwt", "vel")
    # pr.dispersion()
    # depths = [40, 50, 60, 70, 80, 90, 100, 120, 150, 180, 210, 240]
    # pr.mcmc(depths=depths)
    # pr.mcmc(linetypes=["arise", "decline", "xline", "yline"])


if __name__ == "__main__":
    main()
