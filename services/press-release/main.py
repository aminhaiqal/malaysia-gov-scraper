import argparse
from src.scheduler import run_all


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Run scraping once')
    args = parser.parse_args()
    if args.once:
        run_all()
    else:
        # simple loop - in production use cron or k8s CronJob
        import time
        while True:
            run_all()
            time.sleep(60 * 60) # run hourly


if __name__ == '__main__':
    main()