/* WebSpeech.ready(function () {
    WebSpeech.server = 'http://120.24.87.124/cgi-bin/ekho2.pl';
    WebSpeech.setVoice('EkhoCantonese')
    WebSpeech.setSpeedDelta(-15)
}) */
const synth = window.speechSynthesis;
const voices = window.speechSynthesis.getVoices();
console.log(voices)
let speakButtons = document.querySelectorAll(".speak");
console.log(speakButtons);
let voice = 1

speakButtons.forEach(function (button, index) {
    button.addEventListener("click", function (e) {
        e.preventDefault();
        //console.log(document.getElementById('lyrics' + (index + 1).toString()).value)
        /* WebSpeech.speak(e.target.parentElement.previousElementSibling.innerText); */
        let u = new SpeechSynthesisUtterance();
        u.id = (index + 1).toString();
        u.onboundary = onboundaryHandler;
        u.lang = 'zh-HK';
        //synth.getVoices().forEach((e, idx) => voice = (e.lang == u.lang) ? idx : voice)
        console.log(voice)
        u.voice = synth.getVoices()[voice];
        if (u.voice.lang != 'zh-HK'){
           u.voice = synth.getVoices()[17]
        }
        console.log("test")
        console.log(u.voice)
        u.text = document.getElementById('lyrics' + (index + 1).toString()).
            value
        synth.cancel();
        synth.speak(u);
    });
});

let dropdown = document.querySelector("#dropdown")
dropdown.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector("#voices").classList.toggle("hidden");
})
let dropdown_options = document.querySelectorAll(".voice");
dropdown_options.forEach(function (option) {
    option.addEventListener("click", function (e) {
        e.preventDefault();
        voice = option.value
        console.log("change voice")
        document.querySelector("#voices").classList.toggle("hidden")
    });
})

function onboundaryHandler(event) {
    var textarea = document.getElementById('lyrics' + event.utterance.id)
    var value = textarea.value;
    console.log(value)
    var index = event.charIndex;
    var word = getWordAt(value, index);
    var anchorPosition = getWordStart(value, index);
    var activePosition = anchorPosition + word.length;

    textarea.focus();

    if (textarea.setSelectionRange) {
        textarea.setSelectionRange(anchorPosition, activePosition);
    }
    else {
        var range = textarea.createTextRange();
        range.collapse(true);
        range.moveEnd('character', activePosition);
        range.moveStart('character', anchorPosition);
        range.select();
    }
};


// Get the word of a string given the string and index
function getWordAt(str, pos) {
    // Perform type conversions.
    str = String(str);
    pos = Number(pos) >>> 0;

    // Search for the word's beginning and end.
    var left = str.slice(0, pos + 1).search(/\S+$/),
        right = str.slice(pos).search(/\s/);

    // The last word in the string is a special case.
    if (right < 0) {
        return str.slice(left);
    }

    // Return the word, using the located bounds to extract it from the string.
    return str.slice(left, right + pos);
}

// Get the position of the beginning of the word
function getWordStart(str, pos) {
    str = String(str);
    pos = Number(pos) >>> 0;

    // Search for the word's beginning
    var start = str.slice(0, pos + 1).search(/\S+$/);
    return start;
}


//to be implemented
/* document.getElementById('pauseButton').onclick = function(){
    if (speechSynthesis) {
      speechSynthesis.pause();
    }
};

document.getElementById('resumeButton').onclick = function(){
    if (speechSynthesis) {
      speechSynthesis.resume();
    }
};

document.getElementById('stopButton').onclick = function(){
    if (speechSynthesis) {
      speechSynthesis.cancel();
    }
}; */
