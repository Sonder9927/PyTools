from src.plot_results import Painter


def main():
    pr = Painter()
    # pr.initialize(lab_range=[-50, -150])
    pr.mcmc(profile=True)
    # pr.phase("diff", periods=[20])
    # pr.area("sites")
    # pr.phase("cb", "tpwt", dcheck=1.5)
    # pr.dispersion()
    # depths = list(range(10, 210, 10))
    # pr.mcmc(depths=depths)


if __name__ == "__main__":
    main()
