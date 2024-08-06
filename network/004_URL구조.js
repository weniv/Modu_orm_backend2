const url = new URL(
    'https://www.example.com/path/to/page?key1=value1&key2=value2#section',
);

console.log(url.protocol); // "https:"
console.log(url.hostname); // "www.example.com"
console.log(url.pathname); // "/path/to/page"
console.log(url.search); // "?key1=value1&key2=value2"
console.log(url.hash); // "#section"