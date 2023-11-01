from src.plot_results import Painter


def main():
    pr = Painter()
    # pr.area("model")
    # pr.phase("cb", "tpwt", dcheck=1.5)
    # pr.dispersion()
    # depths = list(range(10, 210, 10))
    pr.mcmc(profile=True)  # , depths=depths)  # , profile=True)


if __name__ == "__main__":
    main()
