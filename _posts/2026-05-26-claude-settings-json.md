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


[settings.json](https://prod-files-secure.s3.us-west-2.amazonaws.com/801d6147-b21d-470e-86f3-97755263bf8d/09c99e67-7a7f-41d8-a5d2-1cf5a3757452/settings.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466UXQRZOSL%2F20260602%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260602T070354Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFQaCXVzLXdlc3QtMiJHMEUCIQCAOg3D%2FJ0mnH0pqgKNBs%2FxvLf6HkKz%2BkitXL6EimTP2QIgLOsgeVdErkyADqBddf5QEIDHavtpqx9XfVjvH7qYlXgq%2FwMIHRAAGgw2Mzc0MjMxODM4MDUiDCTnAkqQCPMh6rlvFyrcAyWSsKYQAxHN8jinZwE5fvysEBRWL7jCULJkAqpGl7M%2Bf%2Bc3P193AxtJX85V%2FmcEqkYw%2BlZ8jdbnE0mUzaZ3%2BWwvgkcQLqKW6RauRnHPaO4hMT2BBCGg%2BpAHmI358zmmkK9L90%2Ft4uyG1p1mIhvkoZeXmHhxrkwx5ggQaX2SE3hXfZQaXFvDJQLTRc1mtFn09i2YrPVwF6MFaDzRYHyHXmcl1KkaLp34V1ooe3PYDCg5cE55vCl6568TXRmKbhC%2FXE73xydvinwitUaYVbHzZbWdPoPxboXLT4Qk3IkXzw5KeZWEicn%2BksKPIDMSBhvab6Lb%2BVefMNd2RyD6jG8gJk8sEhZl4z16%2BDYYfXq8awguEJ%2Fd2aya%2F%2F2FEbiWkExSvSt%2B7%2FzKoL67zZSgdWzYLuNBax50HggDt8rly%2BNgJ9ck8RMXTNZjIJjE12xNrYFSOactXUZza%2BZ%2BqVlYIMpcDdBhge0KZuguJr6fvDWvab%2Fqya3e9E%2Bssi2EQYwVHn7v5BDbiZj0651LQeJko0jjp6lj6YMv61EHR8y5JkvWQIycvKUHaF54YcZk7DbtG61Byvbuyd%2BLfc6RZQKrO5jd1ZMWtafCSTqaynj1b8D%2BLsDv8Cbv7uTHqxs1FbQeMNij%2BdAGOqUBIM%2FnjWjn7MZQC4hdyPPnmmPsWV2DGbC%2FgT9JyKV%2FpBTC5UMDYE%2BOkdjGP4HjKbBZBVc74isMzsqwJHAsEVeWrA6uWkoROq29Bre7yQ2aNdHoUAAyseRAflDTkIMRJhUfmoOnB6uCI5ZNyVqA5Xr7HSWK9jRBUGtHZbqp%2FCHFKEnmjyxTDzl%2Fx7pd6LVBq0cCQbvHzlNKgLME2f9L%2BQQbpsaz6ecd&X-Amz-Signature=f26ea2d139c79faf66cfb0a9135c382a0a4e6c0525ee1178b7f4909ca47ee68b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)


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
