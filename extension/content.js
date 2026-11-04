console.log("IntelliLeak Extension Loaded");

let previousPrompt = "";
let latestResult = null;
let lastWarningHash = "";

let allowNextSubmission = false;

function initializeIntelliLeak() {


    setInterval(
        monitorPrompt,
        1000
    );

}

initializeIntelliLeak();

async function monitorPrompt() {

    const editor = getEditor();

    if (!editor)
        return;

    const prompt = getPromptText();

    if (!prompt) {

        previousPrompt = "";
        latestResult = null;

        return;

    }

    // Ignore unchanged prompt
    if (prompt === previousPrompt)
        return;

    previousPrompt = prompt;

    console.log("Monitoring:");
    console.log(prompt);

    const result =
        await analyzePrompt(prompt);

    if (!result)
        return;


    latestResult = result;

    const currentHash =
    JSON.stringify(result);

    if(currentHash === lastWarningHash){

        return;

    }

    lastWarningHash = currentHash;

    console.log(
        JSON.stringify(result, null, 2)
    );

}

/*
    IntelliLeak Submission Interceptor
*/

function interceptSubmission(event) {

    // User already confirmed once
    if (allowNextSubmission) {

        allowNextSubmission = false;

        console.log("Submission allowed after confirmation.");

        return;

    }

    
    if (!latestResult)
        return;

    // Only warn for MEDIUM / HIGH / CRITICAL
    if (
        latestResult.risk_level === "SAFE" ||
        latestResult.risk_level === "LOW"
    ) {
        console.log("Low-risk prompt. Submission allowed.");
        return;
    }

    // Stop ChatGPT from sending
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();

    showWarningDialog(

        latestResult,

        () => {

            allowNextSubmission = true;

            console.log("User chose to continue.");

        }

    );

}

/*
    Detect Send Button Chatgpt
*/

document.addEventListener(

    "pointerdown",

    function(event){

        if(getCurrentPlatform() !== "chatgpt")
            return;

        const button = event.target.closest(
            "#composer-submit-button"
        );

        if (!button)
            return;

        interceptSubmission(event);

    },

    true

);

/*
    Detect Send Button Gemini
*/

document.addEventListener(

    "pointerdown",

    function(event){

        if(getCurrentPlatform() !== "gemini")
            return;

        const gemButton =
            event.target.closest("button");

        if(!gemButton)
            return;

        if(
            gemButton.getAttribute("aria-label") !== "Send message"
        )
            return;

        console.log("Gemini Send detected");

        interceptSubmission(event);

    },

    true

);

/*
    Detect Enter Key
*/

document.addEventListener(

    "keydown",

    function(event){

        if (
            event.key !== "Enter" ||
            event.shiftKey
        )
            return;

        const editor =
            getEditor();

        if (
            !editor ||
            !editor.contains(
                document.activeElement
            )
        )
            return;

        interceptSubmission(event);

    },

    true

);
