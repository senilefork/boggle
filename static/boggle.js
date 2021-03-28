let score = 0;
let seconds = 0;
let words = new Set();

function timer(){
    setInterval(async function(){
        seconds += 1;
        $('#time').text(`${seconds}`);
        if(seconds === 30){
            let resp = await trackScore();
            //console.log(test.score)
            clearInterval(timer);
            alert(`GAME OVER Score: ${resp.data.score}`);
            location.reload();
        }
    },1000)
}

function message(msg,cl){
    $('#message').text(msg).addClass(cl);
}

async function handleClick(e){
    e.preventDefault();

    let word = $('#user-input').val();
    const response = await axios.get('/check-word',{params :{ words:word }});

    if(response.data.server === "ok"){
        if(words.has(word)){
            message("You already guessed that word, try again...", "error");
        } else {
        words.add(word);
        message('Nice one','success');
        $('#word-list').append(`<li>${word}</li>`);
        score += word.length;
        $('#current-score').text(`${score}`)
        $('#form').trigger('reset');
        }
    } 
    if(response.data.server === "not-on-board"){
        message("That word isn't on the board, try again...", "error");
    }
    if(response.data.server === "not-word"){
        message("Not an english word, try again...", "error");
    }
}

document.getElementById('form').addEventListener('submit', handleClick);

async function trackScore(){
    let resp = await axios.post('/score', {scores:score})
    console.log(resp)
    console.log(resp.data)
    console.log(resp.data.score)
    return resp;
}

timer();
