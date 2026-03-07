import hashlib
import subprocess


def generate_provenance_hash(data_path: str, config_path: str):
    """Generate a composite hash of code, data, and config."""
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except:
        git_hash = "no-git-repo"

    with open(data_path, "rb") as f:
        data_hash = hashlib.sha256(f.read()).hexdigest()

    with open(config_path, "rb") as f:
        config_hash = hashlib.sha256(f.read()).hexdigest()

    composite = f"{git_hash}-{data_hash}-{config_hash}"
    return hashlib.sha256(composite.encode()).hexdigest()


if __name__ == "__main__":
    # Example usage
    # h = generate_provenance_hash("data/processed/dummy.csv", "configs/base.yaml")
    print("Provenance Engine Active.")
