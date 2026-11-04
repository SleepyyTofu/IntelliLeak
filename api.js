/*
    IntelliLeak API Module
*/

async function analyzePrompt(prompt) {

    return new Promise((resolve) => {

        chrome.runtime.sendMessage(

            {

                action: "analyzePrompt",

                prompt: prompt

            },

            function(response){

                resolve(response);

            }

        );

    });

}