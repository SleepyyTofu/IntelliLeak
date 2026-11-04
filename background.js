/*
    IntelliLeak Background Service Worker
*/

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    if (request.action !== "analyzePrompt")
        return;

    fetch("http://127.0.0.1:5000/analyze_prompt", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            prompt: request.prompt

        })

    })

    .then(response => response.json())

    .then(data => {

        sendResponse(data);

    })

    .catch(error => {

        console.error(error);

        sendResponse(null);

    });

    return true;

});