---
layout: post
title: "API / REST API"
description: "API는 서버와 통신하는 모든 방법의 큰 범주이고, REST는 그중 'URI=대상, 메서드=동작' 규칙으로 만든 가장 널리 쓰이는 스타일이다. 차이와 그렇게 쓰는 이유 정리."
date: 2026-06-19
categories: ["1.Backend", "spring"]
tags: ["api", "rest"]
---


API 랑 REST API 에 개념을 한번 짚고 가자!!!


## **1. API?**


**API(Application Programming Interface)** 는 _서버랑 통신하는 모든 방법을 통칭하는 큰 범주_다.


## **2. REST API?**


**REST는 API를 만드는 여러 방식 중 "가장 널리 쓰이는 한 가지 규칙(스타일)"** 이다.

- **URI(주소)** → "무엇을(대상)"
- **HTTP 메서드** → "어떻게(동작)"

REST는 **동작(CRUD)마다 메서드가 따로 있다.**


| **하고 싶은 것** | **메서드**         | **예시**            |
| ----------- | --------------- | ----------------- |
| 조회 (Read)   | `GET`           | `GET /users/1`    |
| 생성 (Create) | `POST`          | `POST /users`     |
| 수정 (Update) | `PUT` / `PATCH` | `PUT /users/1`    |
| 삭제 (Delete) | `DELETE`        | `DELETE /users/1` |

> **주소가 똑같아도, 메서드만 바꾸면 다른 동작이 된다.**  
> 주소는 다 `/users/1`(대상)인데, 앞에 붙는 메서드가 "무엇을 할지"를 결정한다.

```java
GET    /users/1   →  1번 유저 조회
PUT    /users/1   →  1번 유저 수정
DELETE /users/1   →  1번 유저 삭제
```


### **PUT vs PATCH (헷갈리는 포인트)**

- **PUT** = 전체 교체 (모든 필드를 다 보냄)
- **PATCH** = 일부만 수정 (바뀐 필드만 보냄)

```java
PUT   /users/1  { "name": "철수", "age": 20, "email": "..." }  // 전체 덮어쓰기
PATCH /users/1  { "age": 21 }                                  // 나이만 변경
```

> POST/GET만 자주 보이는 이유는, 옛날 HTML `<form>`이 GET/POST만 지원했던 습관이 남았기 때문이다.   
> 제대로 된 REST라면 수정엔 PUT/PATCH, 삭제엔 DELETE를 쓰는 게 맞다.

## **3. REST API 쓰는 이유?**


처음엔 "그냥 다 POST로 하면 편하지 않나?" 싶다. 하지만 **살짝 귀찮은 대가로 나중에 훨씬 편해지는** 구조다.


### **① 안 나누면 처음만 편하고 나중이 지옥이다**


규칙 없이 만들면 기능마다 주소를 **창작**해야 한다.


`POST /getUserPOST /updateUserNamePOST /deleteUserPOST /getUserList...`


이름이 제각각이라 3개월 뒤엔 본인도 헷갈리고, 협업하면 더 심해진다. 
REST로 하면 주소는 `/users` 하나로 고정, 동작은 메서드로 처리하니 **외울 게 없다.**


### **② 메서드마다 "성격"이 정해져 있어서 공짜로 얻는 게 많다**


HTTP 메서드는 그냥 이름표가 아니라 **약속된 성질**이 있다.


| **메서드**              | **성질**              | **실무에서 얻는 이득**           |
| -------------------- | ------------------- | ------------------------ |
| `GET`                | 안전(읽기만) · 캐싱 가능     | 브라우저/CDN이 자동 캐싱 → 성능↑    |
| `GET` `PUT` `DELETE` | 멱등(여러 번 호출해도 결과 같음) | 재시도해도 안전                 |
| `POST`               | 멱등 아님               | "결제처럼 중복되면 안 되는 것"으로 구분됨 |


전부 POST로 하면 이 구분이 사라져서, 브라우저도 CDN도 "읽기인지 쓰기인지" 몰라 최적화를 하나도 못 해준다.


### **③ 메서드가 곧 "문서"다**


`DELETE /users/1`


주석 없이 봐도 "1번 유저 삭제"가 바로 읽힌다. 반면 `POST /process`는 까보기 전엔 뭘 하는지 모른다.


## **4. Spring에서는 어떻게? (같은 주소, 메서드만 분리)**


**Spring을 쓰면 더 나누는 게 귀찮지도 않다.** 같은 엔드포인트(URI)라도 메서드만 다르면 알아서 분리해준다.


```java
@RestController@RequestMapping("/users")
public class UserController {
    @GetMapping("/{id}")        // GET    /users/1 → 여기로    
    public UserDto get(@PathVariable Long id) { ... }
    
    @PutMapping("/{id}")        // PUT    /users/1 → 여기로    
    public UserDto update(@PathVariable Long id, @RequestBody UserUpdateRequest req) { ... }
    
    @DeleteMapping("/{id}")     // DELETE /users/1 → 여기로    
    public void delete(@PathVariable Long id) { ... }
}
```


URI는 셋 다 `/users/1`로 똑같지만, 들어온 요청의 **메서드(GET/PUT/DELETE)를 보고 Spring이 알맞은 핸들러로 보내준다.** if문으로 분기할 필요가 없다.


## **5. 정리**

- **API** = 통신하는 모든 방법을 통칭하는 큰 범주
- **REST API** = 그 통신을 "주소는 대상, 메서드는 동작"이라는 약속대로 깔끔하게 만든 것
- REST는 새로운 기술이 아니라 **"이렇게 좀 통일해서 만들자"는 스타일/약속**
- 살짝 규칙을 지키는 대가로 → **예측 가능 + 캐싱/재시도 최적화 + 문서화 효과 + 협업 편의**를 공짜로 얻는다
- Spring에선 `@GetMapping`, `@PostMapping`... 어노테이션만으로 같은 주소를 동작별로 깔끔하게 분리할 수 있다
> 처음엔 "굳이 나눠야 하나" 싶지만, 나눠두면 나중에 안 꼬인다. 그래서 다들 REST를 기본으로 깔고 간다.
