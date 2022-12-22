export function flushPromises() {
    return new Promise(function (resolve) {
        setTimeout(resolve);
    });
}
// Vue test utils component selection
export function componentWithText(wrapperArray, text) {
    return wrapperArray.filter((c) => c.text().includes(text)).at(0);
}
//# sourceMappingURL=utils.js.map