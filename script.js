
/* Constants */

/*Button Text*/
var musicOnText = "Music "+" \u{1F50A}";
var musicOffText = "Music "+" \u{1F507}";
var portfolioText = "Portfolio"+" \u{1F4BC}";
var resumeText = "Resume"+" \u{1F4C3}";

/* Element Initialization */
var musicButton = document.getElementById('musicButton');
var cvButton = document.getElementById('cvButton');
var portfolioButton = document.getElementById('portButton');

musicButton.innerText= musicOffText;
cvButton.innerText= resumeText;
portfolioButton.innerText = portfolioText;

var playing = false;
var songAudio = null;

/* Music Button */
function playMIDI() {
    if (songAudio){
        songAudio.pause();
        songAudio = null;
        musicButton.innerText = musicOffText;
        return;
    }
    songAudio = new Audio('music/passport.m4a');
    songAudio.loop = true;
    songAudio.play();
    musicButton.innerText= musicOnText;
}