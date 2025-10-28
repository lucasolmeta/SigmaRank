from src.backtest import engine, metrics
from src.portfolio import construction, ranking, mc_sizer
from src.risk import cov_estimation, vol_target

def main():
    engine.main()

    metrics.main()

    construction.main()

    ranking.main()

    mc_sizer.main()

    cov_estimation.main()
    
    vol_target.main()


if __name__ == '__main__':
    main() 