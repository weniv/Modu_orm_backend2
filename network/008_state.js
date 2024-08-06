// step1: 회원 가입 fetch를 이용한 POST 요청
fetch('https://eduapi.weniv.co.kr/1/signup', {
method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'test1',
        password: 'test1234',
    }),
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));

fetch('https://eduapi.weniv.co.kr/1/signup', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'test2',
        password: 'test1234',
    }),
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));

// step2: 회원가입이 제대로 되었는지 확인하기 위한 GET 요청
fetch('https://eduapi.weniv.co.kr/1/login_user_info')
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));

// step3: 로그인 fetch를 이용한 POST 요청
fetch('https://eduapi.weniv.co.kr/1/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'test1',
        password: 'test1234',
    }),
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));

// 이곳에서 토큰을 어딘가에 저장해야 함

// step4: 로그인이 제대로 되었는지 확인하기 위한 POST 요청(Bearer Token 필요)
fetch('https://eduapi.weniv.co.kr/login_confirm', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer eyJhbGciOi.weniv.h8t7NJKEiWCh7G3',
    },
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));