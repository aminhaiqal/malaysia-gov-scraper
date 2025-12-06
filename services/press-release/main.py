import argparse
from src.scheduler import run_all

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='Run scraping once')
    parser.add_argument('--target', type=str, help='Run a specific scraper by name, e.g., mof, moh, miti, bnm')
    args = parser.parse_args()

    if args.once:
        run_all(target=args.target)
    else:
        # simple loop - in production use cron or k8s CronJob
        import time
        while True:
            run_all(target=args.target)
            time.sleep(60 * 60)  # run hourly

if __name__ == '__main__':
    main()

# python main.py --once --target mof