# -*- coding: utf-8 -*-
"""카드 없는 입간판 합성 — 로컬/Action에서 텍스트 구운 이미지 4장 생성.

글당: og/{id}/h.jpg (히어로) + b1/b2/b3.jpg (본문) — 모두 텍스트 baked.
저장소에 두고 jsDelivr CDN으로 서빙(/media → jsDelivr 리다이렉트).
R2 켜지면 이 경로 그대로 R2로 옮기면 됨.

id = djb2(slug)  (src/lib/body-photos.ts slugImageId 와 동일 해시)
"""
from __future__ import annotations

import os
from pathlib import Path

from keyword_variants import region_leaf
from image_pool import pick_photo_key, POOL_SIZE
from og_compose import compose_for_site

BRAND = "다올스카이차"
PHONE = "010-2445-1554"
SITE_DOMAIN = "daolsky1.co.kr"

BOARD_MAP = {
    "스카이차": ("스카이차", "스카이차"),
    "스카이차 일대": ("일대", "스카이차"),
    "스카이 작업차": ("작업차", "스카이차"),
    "스카이차 요금": ("요금", "스카이차"),
    "스카이차 비용": ("비용", "스카이차"),
    "스카이차 가격": ("가격", "스카이차"),
    "스카이차 이용료": ("이용료", "스카이차"),
    "고소작업차량": ("차량", "고소작업"),
}


def _djb2(s: str) -> int:
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return h


def _split_board(board_title: str):
    return BOARD_MAP.get(board_title, (board_title, board_title))


def _pick_body_photos(slug: str, hero_n: int, count: int = 3):
    used = {hero_n}
    picked = []
    seed = 0
    while len(picked) < count and seed < POOL_SIZE * 2:
        n = (_djb2(f"{slug}#body{seed}") % POOL_SIZE) + 1
        if n not in used:
            used.add(n)
            picked.append(n)
        seed += 1
    return picked


def compose_post_images(slug: str, region: str, board_title: str,
                        photos_dir: str | None = None, repo_root: str | None = None) -> str:
    """4장 합성 후 repo_root/og/{id}/ 에 저장. 히어로 /media URL 반환.

    photos_dir/repo_root 미지정 시 저장소 구조(../photos, ..)에서 자동 추론.
    """
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[1]
    photos_dir = photos_dir or str(root / "photos")
    repo_root = str(root)
    img_id = _djb2(slug)
    ribbon, head_main = _split_board(board_title)
    prefix = region_leaf(region)
    out_dir = Path(repo_root) / "og" / str(img_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    def _src_bytes(n: int) -> bytes:
        return (Path(photos_dir) / f"{n:03d}.jpg").read_bytes()

    def _compose(n: int) -> bytes:
        return compose_for_site(
            SITE_DOMAIN, _src_bytes(n),
            ribbon=ribbon, headline_prefix=prefix, headline_main=head_main,
            brand_name=BRAND, phone=PHONE,
        )

    hero_n = int(pick_photo_key(slug).split("/")[-1].split(".")[0])
    (out_dir / "h.jpg").write_bytes(_compose(hero_n))
    for i, n in enumerate(_pick_body_photos(slug, hero_n), 1):
        (out_dir / f"b{i}.jpg").write_bytes(_compose(n))

    return f"/media/og/{img_id}/h.jpg"


if __name__ == "__main__":
    import sys
    # 단일 글 합성: argv = slug, region, board_title
    slug, region, board = sys.argv[1], sys.argv[2], sys.argv[3]
    repo = Path(__file__).resolve().parents[1]
    url = compose_post_images(slug, region, board, str(repo / "photos"), str(repo))
    print("hero_url =", url)
    print("saved to:", repo / "og" / str(_djb2(slug)))
