/*
    IntelliLeak
    Platform Detection Module
*/

function getCurrentPlatform() {

    const host = window.location.hostname;

    if (
        host.includes("chatgpt.com") ||
        host.includes("chat.openai.com")
    ) {
        return "chatgpt";
    }

    if (
        host.includes("gemini.google.com")
    ) {
        return "gemini";
    }

    return "unknown";

}


/*
    Prompt Editor
*/

function getEditor() {

    const platform =
        getCurrentPlatform();

    switch (platform) {

        case "chatgpt":

            return document.querySelector(
                "#prompt-textarea"
            );

        case "gemini":

            return document.querySelector(
                '[contenteditable="true"]'
            );

        default:

            return null;

    }

}


/*
    Prompt Text
*/

function getPromptText() {

    const editor =
        getEditor();

    if (!editor)
        return "";

    return (
        editor.innerText ||
        editor.textContent ||
        ""
    ).trim();

}