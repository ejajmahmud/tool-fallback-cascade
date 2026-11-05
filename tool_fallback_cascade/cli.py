"""CLI for tool-fallback-cascade."""
import sys
import argparse
from .cascade import FallbackCascade


def main():
    parser = argparse.ArgumentParser(description="Tool Fallback Cascade")
    parser.add_argument("--demo", action="store_true", help="Run fallback cascade demonstration")
    args = parser.parse_args()

    cascade = FallbackCascade("weather_service")
    if args.demo:
        def primary():
            raise ConnectionError("Primary weather provider unavailable")
        def secondary():
            return {"temp": 21, "source": "backup_weather"}

        cascade.add_handler("primary_api", primary)
        cascade.add_handler("backup_api", secondary)
        res = cascade.execute()
        print("Execution Result:", res)
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
