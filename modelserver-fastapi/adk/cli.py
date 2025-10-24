"""ADK CLI module.

Run with:
  cd modelserver-fastapi
  source .venv/bin/activate
  python -m adk api_server --port 9000
"""
from __future__ import annotations

import argparse
import os


def run_api_server(host: str, port: int, reload: bool):
    try:
        import uvicorn
    except Exception:
        print("uvicorn is not installed in the active environment. Install with: pip install uvicorn")
        raise

    # Ensure working dir is the package root so imports resolve
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(script_dir)

    print(f"Starting ADK quickstart server on {host}:{port} (reload={reload})")
    uvicorn.run("adk_quickstart:app", host=host, port=port, reload=reload)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="adk", description="ADK development CLI")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    api_parser = subparsers.add_parser("api_server", help="Start the ADK quickstart FastAPI server")
    api_parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    api_parser.add_argument("--port", default=9000, type=int, help="Port to bind")
    api_parser.add_argument("--reload", action="store_true", help="Enable uvicorn reload (dev only)")

    args = parser.parse_args(argv)

    if args.cmd == "api_server":
        run_api_server(args.host, args.port, args.reload)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
