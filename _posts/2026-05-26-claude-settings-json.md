---
layout: post
title: "Claude/settings.json 설정 가이드"
description: "Claude Code의 자동 허용·차단 목록을 설정하여 작업 팝업을 없애고 위험 명령을 차단하도록 하는 ~/.claude/settings.json 파일 사용 가이드."
date: 2026-05-26
categories: ["AI", "Claude(Code)"]
tags: ["설정"]
---


# ~/.claude/settings.json 설정 가이드


## 1. 이 파일이 뭐야?


Claude Code가 작업할 때 매번 "이거 실행해도 돼요?" 허용 팝업이 뜨는데,
이 파일에 미리 허용/차단 목록을 정해두면 팝업 없이 자동으로 처리된다.


에이전트(PM/Developer/Publisher/QA)가 자율적으로 작업할 때
**사람이 일일이 허용 누르는 수고 없이** 돌아가게 하되,
**위험한 명령은 아예 못 하도록** 막는 게 목적.


## 2. 파일 및 위치정보


[settings.json](https://prod-files-secure.s3.us-west-2.amazonaws.com/801d6147-b21d-470e-86f3-97755263bf8d/09c99e67-7a7f-41d8-a5d2-1cf5a3757452/settings.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466UPU4KGF6%2F20260602%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260602T054535Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFIaCXVzLXdlc3QtMiJIMEYCIQDcRk7reZFWjHgeekfI3SSlDox8wyw%2BDp0%2FHGgdbHdy3wIhAJBiOF8rfYl%2B4I%2FPgcO7j32Yz%2Fvz3UMEeAoVsHOfZbayKv8DCBsQABoMNjM3NDIzMTgzODA1IgyEwtHCsU9v35DA2Lkq3AMsrV1Tom1yLc8tUqiqx4x97jhM91kKkWDRUaQ49FQnVrLL2cJt68oa7vwW4vHAKWtXsR2BHC46vxK7zDdV%2FDLDhW2aVNp1G5ZGVDlGXaolzfT4Hx78abvCjX8Cn1OZNcG2FeJrEKzOY%2FLpEeycCKYtwS2d69GSDHK3XiKg7JaFSO1Y6S5AZUNon2e0DNMqtI48z3HNOgdczqtFCkriQ4%2F8mk6TYWdUxvonkKwilKDKq7OUSagclSBKCwRdj98E2Byr9Xr9m0LyTAn0A%2FFrZkuTTTxmAKQac4%2FcEHITB96BCfGJm4T1ff5cDWGyeqjDkwccn1EXJKnEEooUjyRquM1dwzVJuN7zwrMI4L0wkDXCx%2ByA7ffh%2B7ZQHcIhvVEDeEXuGbaOO0ccvX4zP4tJZ16MvUEAoDrASadrYXp2ESoEYvSDLH7PT9MxhahyXDCeqMSfZmcMXQh8EVPvkCoLoeJPFh0W91Z3%2Fh8wr8%2FV%2FIVKdbTwX8LDC1DrU%2FVweFjFihgsR45qwNphOa6z07wniXBRCJ3SEkjFWZjZb7x0hEDlk6ZR0d%2Fgg%2BsvOQwQpF6CGZwbRHM3%2FGOh7IqJ5lkAn6Cl0MXCJc7ktcfatDY3ONI0cNRM5PrqdiThaPxkbDCh9PjQBjqkATKgJXl8y%2FnAUmxMPNfCLff9GXTgXsJLi1WnxHpmuemkpSfQZZhztIGTQbhvjCKh4no7xe8s4X6ks8hkv%2Fa050KvV1Dh5Az2Cx2IkSALLdJoL%2BPymja7bb2T85i8CYNXoPkS35tFcx2SLNeldrKaJ33XrUw79IcOF%2Bu5GAxjg4ORm%2BOZ6E%2BqQkIdzPPB%2BoyW3EJ8AMls19yEeZgo5Smsk0yZH8ju&X-Amz-Signature=7df5dda8cdbfb3a578f3ca79a6fcf9e51a54f6dde652165755167a9127131f45&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)


```shell
~/.claude/
├── agents/
│   ├── pm_orchestrator.md
│   ├── developer.md
│   ├── ui_publisher.md
│   └── reviewer_qa.md
└── settings.json   ← 여기
```


## 3. 파일설명


**허용 (자동 통과)**

- `git add / status / diff / log / branch / checkout / stash` — 조회·스테이징만
- 파일 읽기/쓰기/수정/복사/이동
- `ls / cat / find / grep` — 탐색
- `npm / gradlew / mvn` — 빌드·실행

**차단 (자동 거부)**

- `git commit / push / rebase / reset / clean` — 커밋·히스토리 조작
- `rm / rmdir` — 삭제
- `chmod / chown / sudo` — 권한 변경
- `curl / wget` — 외부 네트워크 요청 (에이전트가 외부에서 뭔가 몰래 받아오는 거 방지용,필요하면 allow로 옮기기)
- `dd / mkfs` — 디스크 조작
