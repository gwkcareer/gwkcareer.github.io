---
layout: post
title: "왜 GitLab(형상관리)에 Properties 파일을 올리면 안 될까?"
description: "Git은 이력을 영구 보관하므로 한 번 올라간 Secret은 삭제해도 사라지지 않는다. Properties 파일의 비밀번호·API Key·토큰은 코드가 아닌 보안 저장소로 분리해야 한다."
date: 2026-06-25
categories: ["1.Backend", "보안"]
tags: ["GitLab"]
---


## **왜 이게 문제가 될까?**


최근 공공기관을 중심으로 "소스코드 저장소(GitLab, GitHub 등)에 프로퍼티 파일을 올리지 말라"는 보안 지침이 강화되고 있다. 특히 대규모 개인정보 유출 사고 이후 많은 기관과 기업에서 소스코드 관리 정책을 다시 점검하고 있다.


단순한 텍스트 파일 하나가 왜 문제가 되는 걸까?


```java
spring.datasource.url=jdbc:mysql://...
spring.datasource.username=admin
spring.datasource.password=1234
jwt.secret=xxxxxxxxxxxxxxxx
aws.accessKey=xxxxxxxxxxxxxxxx
aws.secretKey=xxxxxxxxxxxxxxxx
```


개발할 때는 편리하지만, 보안 측면에서는 매우 위험하다.


## **이유 1 — Git은 삭제해도 이력이 남는다**


Git은 모든 변경 이력을 영구 보관한다. 실수로 비밀번호를 커밋한 뒤 바로 삭제해도 과거 커밋을 조회하면 다시 확인할 수 있다.


```java
git log
git checkout <이전 커밋 해시>
```


**한 번 올라간 Secret은 이미 유출된 것으로 간주해야 한다.**


이미 저장소에 올라간 적이 있는 Secret은 즉시 폐기하고 새로 발급해야 한다. 단순히 파일을 지우는 것으로는 충분하지 않다.


## **이유 2 — 저장소에 접근하는 사람은 모두 확인 가능하다**


사내 GitLab이라도 다양한 사람이 접근한다.

- 개발자 / 운영 담당자
- 협력업체 / 외주 개발자
- 시스템 관리자

운영 DB 계정이나 API Key가 파일에 담겨 있다면, 저장소 접근 권한만으로 중요한 시스템 정보가 그대로 노출된다.


## **이유 3 — Secret 하나가 전체 시스템으로 이어진다**


프로퍼티 파일에 담기는 민감 정보는 생각보다 범위가 넓다.

- DB 계정(MySQL, Oracle, Redis 등)
- Kafka, SMTP 연결 정보
- JWT Secret, OAuth Client Secret
- AWS Access Key / Azure Key
- 암호화 키

이 중 하나만 노출되어도 개인정보 무단 조회, 데이터 삭제, 토큰 위조, 클라우드 자원 무단 사용 등으로 이어질 수 있다.


## **이유 4 — 형상관리는 코드를 관리하는 곳이지, 비밀을 보관하는 곳이 아니다**


**코드와 Secret을 분리하는 것이 기본 원칙**이다. 민감 정보는 아래 방식으로 분리 관리한다.

- **환경 변수** — 서버에서 직접 주입
- **GitLab CI/CD Variables** — 파이프라인 실행 시 주입
- **HashiCorp Vault** — 중앙 집중형 Secret 관리
- **Kubernetes Secret** — 컨테이너 환경
- **AWS Secrets Manager / Azure Key Vault** — 클라우드 환경

## **이유 5 — 실제 공격도 Git 저장소에서 시작된다**


공격자에게는 소스코드보다 인증 정보(Secret)가 훨씬 가치 있다. 실제 침해 사고의 흐름은 다음과 같다.


```java
Git 저장소 접근 → Secret 획득 → 운영 서버 접속 → DB 접근 → 개인정보 유출
```


저장소가 뚫리는 경로도 다양하다. "내부 GitLab이라 괜찮겠지"는 오해다.

- 계정 탈취 / 관리자 PC 악성코드 감염
- 협력업체 계정 유출
- 권한 오남용
- 백업 서버 유출

## **올바른 관리 방법**


| **파일**                    | **저장소 포함** | **설명**                  |
| ------------------------- | ---------- | ----------------------- |
| `application.yml`         | 조건부        | 민감 정보 없이 구조만            |
| `application-example.yml` | O          | 예시 값만 담은 가이드용           |
| `application-local.yml`   | X          | 로컬 개발용, `.gitignore` 처리 |
| 환경 변수                     | —          | 서버/CI에서 직접 주입           |
| Secret Manager            | —          | 클라우드/사내 보안 저장소          |


실제 값은 서버나 CI/CD 환경에서 주입하고, 코드에는 참조만 남긴다.


```java
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
```


## **한 줄 정리**

> 프로퍼티 파일 자체가 문제가 아니라 그 안의 Secret이 문제다. Git은 이력을 영구 보관하므로 한 번 올라간 Secret은 완전히 지우기 어렵고, 접근 권한자 누구나 확인 가능하며, 하나의 유출이 전체 시스템 침해로 이어질 수 있다. 코드는 형상관리로, Secret은 환경 변수나 별도 보안 저장소로 분리하는 것이 표준이다.
