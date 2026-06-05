# -*- coding: utf-8 -*-
import os
import sys
import requests


def normalize_url(url, force_http=False):
    if force_http and url.startswith("https"):
        return url.replace("https", "http", 1)
    return url


def ensure_parent(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent)


def download_simple(url, output_path):
    ensure_parent(output_path)
    response = requests.get(url, headers={
        "Connection": "Keep-Alive",
        "Cache-Control": "max-age=0",
        "Accept": "*/*",
    }, timeout=20)
    response.raise_for_status()
    data = response.content
    with open(output_path, "wb") as fp:
        fp.write(data)
    return len(data)


def get_remote_size(url):
    response = requests.head(url, headers={
        "Connection": "Keep-Alive",
        "Cache-Control": "max-age=0",
        "Accept": "*/*",
    }, timeout=20)
    response.raise_for_status()
    length = response.headers.get("content-length")
    if not length:
        length = response.headers.get("Content-Length")
    return int(length or 0)


def download_range(url, output_path, chunk_size=262144):
    ensure_parent(output_path)
    file_size = get_remote_size(url)
    if file_size <= 0:
        raise RuntimeError("HEAD did not return a valid content-length")

    downloaded = 0
    with open(output_path, "wb") as fp:
        while downloaded < file_size:
            end = min(downloaded + chunk_size - 1, file_size - 1)
            response = requests.get(url, headers={
                "Connection": "Keep-Alive",
                "Cache-Control": "max-age=0",
                "Accept": "*/*",
                "Range": "bytes=%d-%d" % (downloaded, end),
            }, timeout=20)
            response.raise_for_status()
            data = response.content
            if not data:
                raise RuntimeError("range request returned empty data at %d" % downloaded)
            fp.write(data)
            downloaded += len(data)

    return downloaded


def run_case(name, func, url, output_path):
    print("[START] %s" % name)
    print("  url: %s" % url)
    print("  out: %s" % output_path)
    try:
        size = func(url, output_path)
        print("[OK] %s bytes=%s" % (name, size))
    except Exception as exc:
        print("[FAIL] %s: %s" % (name, exc))


def main():
    url = "http://x19.fp.ps.netease.com/file/5a34e09ca7f252df68c974d3i3rv7YsD"
    output_prefix = r"F:\tmp\x19_head_test"

    https_url = normalize_url(url, force_http=False)
    http_url = normalize_url(url, force_http=True)

    cases = [
        ("https_simple_get", download_simple, https_url, output_prefix + "_https_simple.png"),
        ("https_head_range", download_range, https_url, output_prefix + "_https_range.png"),
        ("http_simple_get", download_simple, http_url, output_prefix + "_http_simple.png"),
        ("http_head_range", download_range, http_url, output_prefix + "_http_range.png"),
    ]

    for case in cases:
        run_case(*case)


if __name__ == "__main__":
    sys.exit(main())
