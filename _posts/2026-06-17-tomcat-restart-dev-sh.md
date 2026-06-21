---
layout: post
title: "Tomcat 재기동 셸 스크립트 만들기 (restart_dev.sh)"
description: "개발 톰캣을 재기동할 때마다 PID를 찾아 수동으로 죽이던 작업을, 프로세스 종료·기동·확인까지 한 번에 처리하는 셸 스크립트로 묶은 과정을 정리한다"
date: 2026-06-17
categories: ["3.DevOps", "linux"]
tags: ["Tomcat", "Shell"]
---


개발 톰캣을 재기동할 때마다 `ps`로 PID를 찾고, `kill`로 죽이고, `startup.sh`를 치는 작업을 반복했다. 
매번 손으로 하다 보니 번거롭고 실수도 나와서, 이 과정을 셸 스크립트 하나로 묶었다.


## **기존엔 매번 수동으로**


원래는 이렇게 직접 PID를 찾아 죽이고 다시 올렸다…


```shell
cd /home/tomcat/apache-tomcat-8.5.87/bin/
ps -ef | grep java          # PID 확인
kill -9 145221              # 찾은 PID 종료
./startup.sh                # 다시 기동
```


문제는 재기동할 때마다 PID를 눈으로 찾아 손으로 입력해야 한다는 점이다. 바쁠수록 엉뚱한 프로세스를 죽일 위험도 있다.


## **재기동 스크립트 만들기**


`bin` 디렉토리에서 스크립트 파일을 만든다.


`cd /home/tomcat/apache-tomcat-8.5.87/binvi restart_dev.sh`


`i`로 입력 모드에 들어가 아래 내용을 붙여넣고, `ESC` → `:wq`로 저장한다.


```shell
#!/bin/bash
echo "===== DEV Tomcat Restart ====="
PID=$(ps -ef | grep "Denv=_dev" | grep java | grep -v grep | awk '{print $2}')
if [ -n "$PID" ]; then    echo "Kill PID : $PID"    kill -9 $PID    sleep 5else    echo "DEV Process Not Found"fi
echo "Starting Tomcat..."./startup.sh
sleep 5
NEW_PID=$(ps -ef | grep "Denv=_dev" | grep java | grep -v grep | awk '{print $2}')
if [ -n "$NEW_PID" ]; then    echo "Started Successfully"    echo "PID : $NEW_PID"else    echo "Start Failed"fi
```


## **스크립트가 하는 일**


핵심은 `-Denv=_dev` 옵션으로 dev 프로세스만 골라 잡는 것이다.

- `grep "Denv=_dev"` : 여러 환경이 떠 있어도 dev 프로세스만 선택
- `grep -v grep` : grep 자기 자신은 결과에서 제외
- `awk '{print $2}'` : `ps` 출력에서 PID(두 번째 컬럼)만 추출
- 종료 후 `startup.sh`로 기동하고, 다시 PID를 확인해 정상 기동 여부를 알려준다

## **실행 권한 부여 후 실행**


```shell
chmod +x restart_dev.sh./restart_dev.sh
```


`ls -al restart_dev.sh` 했을 때 권한에 `x`가 보이면(`-rwxr-xr-x`) 준비 완료다.


## **결과 확인**


```shell
ps -ef | grep "Denv=_dev" | grep java
```


PID가 정상적으로 보이면 재기동 성공이다.


## **한 줄 정리**

> 개발 톰캣 재기동을 스크립트 하나로 묶으면 매번 PID를 찾아 죽이는 수고가 사라진다. 
