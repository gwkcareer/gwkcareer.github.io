---
layout: post
title: "Claude/settings.json 설정 가이드"
description: "Claude Code의 자동 허용·차단 목록을 설정하여 작업 팝업을 없애고 위험 명령을 차단하도록 하는 ~/.claude/settings.json 파일 사용 가이드."
date: 2026-05-26
categories: ["AI", "claude"]
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


[settings.json](https://prod-files-secure.s3.us-west-2.amazonaws.com/801d6147-b21d-470e-86f3-97755263bf8d/09c99e67-7a7f-41d8-a5d2-1cf5a3757452/settings.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TIVTODUR%2F20260602%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260602T102646Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFsaCXVzLXdlc3QtMiJGMEQCIGkLI8zGsmL5hwtkfnDdi%2B3Yg9CfU9rK3KOu5q94lnSEAiAbV1qoNZB%2FE%2FRr1cDLyEUiUvZU3nsjqKT%2FrhnAvQbyMSr%2FAwgjEAAaDDYzNzQyMzE4MzgwNSIMdFz60IM4d9XrvY4MKtwDbTDBlDhXY%2FuTNJoP4xLn9iKwynJZiv2tJMt4gnPHqVf81jCIcgFYQN2nLn9Pw54ZrHPaUScLNq6iy1B1kmNzlCTLkrq5MWAlFxN1ZExftXtJpt7mQ330pF%2FWkKc%2FS%2B4tF9BOMhcRL0Sqyy1RrcvXUURn75Nbv2BQFk8TWxgNy04PKKmvhWjOQaWyn8h4vIAykI4xsjW%2F3P71iem83gVQksriThtUOJ3t7a5xmO5YGw%2FRri9KJ%2B8ZDhTL6LOdym6WX4G0eVvhpW477KRymf4rywRlAGO0GlFwvA2tQvq9bqJqy3a8tTECCGQcM5s1CeI4tBY4DEMF4wYYjgVaTT49AcliM4QQWR%2BxUvjhIWfD%2BEX6x%2BIeOtYsrMtlnP%2Fh11talyfmGRJ1JZM7n4pMtGvGI6CNhOwpXnSdkTnAF4OjLIU5gwueFvhwjt8uFW3f5n2xbSk61ISobaNJ0ni4iM%2F77wn9v27IVY%2FsN2x6VMdRw8CWWuXqBFApPflsW8p7zsumMoawxYJIICMoSkGP25jhQxDtH12lRIYOOodH8DYujGKdWQHXw16zKoTPZ3aV%2BzKIaC98sM6f9vQ9K8pONrnveTxbjJDNokdh2mBnfiLYnHt%2FwrPHenTd%2BhirSw8w1d360AY6pgF4%2BRJFNBCGm%2BZoptMPGmgim6ULmK1iKWfGVtptrfZSFSiqs1aF1hxdL44XLV89EQawJP%2BJIgUJZP21%2BocN7LRkb1jxDxeEpaf2%2Fas7u9ZJENWRMypxna%2BhefttHlDIhtWAF1%2FkkLQQZjK%2F01uDw%2Bq%2B8QAEMg80YvFD6JjSr3RInL0kTKKOGx3VHZ9lHWXbjxDpmYKUehSnd%2FrXPvd6wXDbY%2BBjI8kU&X-Amz-Signature=a5f0b846241f2ca26b72327dda06883df2d8308c1b0bf039e428086c19e16899&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)


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
