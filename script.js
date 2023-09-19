var musicButton = document.getElementById('musicButton');
var cvButton = document.getElementById('cvButton');
musicButton.innerText= "Music ❌";
cvButton.innerText= "Resume 📄";
let playing = false;
let songAudio = null;

function playMIDI() {
    if (songAudio){
        songAudio.pause();
        songAudio = null;
        
        musicButton.innerText = "Music ❌";
        return;
    }
    songAudio = new Audio('passport.m4a');
    songAudio.loop = true;
    songAudio.play();
    musicButton.innerText= "Music "+" \u{1F50A}";
}