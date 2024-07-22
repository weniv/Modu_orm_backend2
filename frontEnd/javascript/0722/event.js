
export default function test() {
    const parent = document.querySelector('.parent');

    parent.addEventListener('click', (event) => {
        console.log(this);
        if (event.target.nodeName === "BUTTON") {
            event.target.textContent = "버튼4";
        }
    });
}
