// eduapi.weniv.co.kr
// https://weniv.github.io/weniv_eduAPI/
// 이 페이지에서 CRUD를 연습할 수 있습니다.
// 다만 백엔드 개발자는 fetch를 사용해서 CRUD를 하는 것이 아니라
// 직접 fetch CRUD가 가능하도록 개발해야하는 직군입니다.
// 실제로 이 서버는 fastAPI를 통해 만들어졌습니다.
// 30분마다 초기화되게 설계해두었어요.
// 번호는 직접 선택해서 CRUD 하세요.

fetch("https://eduapi.weniv.co.kr/776/blog")
    .then((response) => response.json())
    .then((json) => console.log(json))
    .catch((error) => console.error(error));


fetch("https://eduapi.weniv.co.kr/776/blog/1")
    .then((response) => response.json())
    .then((json) => console.log(json))
    .catch((error) => console.error(error));


fetch("https://eduapi.weniv.co.kr/776/blog", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            title: "test",
            content: "test",
        }),
    })
    .then((response) => response.json())
    .then((json) => console.log(json))
    .catch((error) => console.error(error));

fetch("https://eduapi.weniv.co.kr/776/blog/1", {
    method: "PUT",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
        title: "test put!!",
        content: "test put!!",
    }),
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));


fetch("https://eduapi.weniv.co.kr/776/blog/1", {
    method: "DELETE",
})
.then((response) => response.json())
.then((json) => console.log(json))
.catch((error) => console.error(error));