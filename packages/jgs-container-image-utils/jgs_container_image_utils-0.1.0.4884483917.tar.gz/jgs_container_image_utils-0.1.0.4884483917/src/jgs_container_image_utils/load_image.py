#!/usr/bin/env python3

import argparse
import json
import subprocess
import tarfile
import typing

def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_name", metavar="image-name")
    parser.add_argument("image_path", metavar="image-path")
    return parser.parse_args()

def get_image_digest(image: str) -> typing.Optional[str]:
    result = subprocess.run(["podman", "images", image, "--format", "{{.Digest}}"], capture_output=True)
    if result.stdout:
        return result.stdout.decode("utf8").strip()

def get_digest_from_archive(archive_path: str) -> str:
    with tarfile.open(archive_path) as fp:
        index_fp = fp.extractfile("index.json")
        js = json.load(index_fp)
        if "manifests" in js and js["manifests"] and "digest" in js["manifests"][0]:
            return js["manifests"][0]["digest"].strip()

def load_archive(archive_path: str):
    print(f"Loading {archive_path}")
    subprocess.run(["podman", "load", "-i", archive_path])

def main():
    args = setup_args()
    image_digest = get_image_digest(args.image_name)
    archive_digest = get_digest_from_archive(args.image_path)
    if image_digest == archive_digest:
        print(f"Not loading {args.image_path} since digests match")
    else:
        load_archive(args.image_path)

if __name__ == "__main__":
    main()
