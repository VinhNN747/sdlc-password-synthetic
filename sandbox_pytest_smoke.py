import asyncio
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from vercel import sandbox
from vercel.sandbox import NetworkPolicy

load_dotenv(Path(__file__).parent / ".env.local")

PROJECT_ROOT = Path(__file__).resolve().parent
SANDBOX_ROOT = "/vercel/password-fixture"
FIXTURE_FILES = (
    ("pyproject.toml", PROJECT_ROOT / "pyproject.toml"),
    ("src/password_policy.py", PROJECT_ROOT / "src/password_policy.py"),
    ("tests/test_password_policy.py", PROJECT_ROOT / "tests/test_password_policy.py"),
)


async def main() -> None:
    async with sandbox.create_sandbox(
        execution_time_limit=timedelta(minutes=5),
    ) as box:
        install = await box.run_command(
            "python",
            ["-m", "pip", "install", "--user", "-q", "pytest==8.4.2"],
            capture_output=True,
            kill_after=90,
        )
        if install.returncode != 0:
            raise RuntimeError(f"Could not install pytest in the sandbox: {install.stderr}")

        await box.update(network_policy=NetworkPolicy.deny_all())
        await box.fs.mkdir(SANDBOX_ROOT, recursive=True)
        for relative_path, local_path in FIXTURE_FILES:
            destination = f"{SANDBOX_ROOT}/{relative_path}"
            await box.fs.mkdir(str(Path(destination).parent), recursive=True)
            await box.fs.write_text(destination, local_path.read_text(encoding="utf-8"))

        result = await box.run_command(
            "python",
            ["-m", "pytest", "-q"],
            cwd=SANDBOX_ROOT,
            capture_output=True,
            kill_after=60,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
        print(f"Sandbox pytest exit code: {result.returncode}")
        if result.returncode != 0:
            raise SystemExit(result.returncode)


asyncio.run(main())
