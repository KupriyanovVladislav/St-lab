function get_value(abbr) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `http://www.nbrb.by/API/ExRates/Rates/${abbr}?ParamMode=2`, false);
    xhr.send();
    if (xhr.status != 200) {
        alert( xhr.status + ': ' + xhr.statusText );
    }
    else {
        data = JSON.parse(xhr.responseText);
        console.log(data.Cur_Scale);
        console.log(data.Cur_OfficialRate);
        result = data.Cur_OfficialRate * data.Cur_Scale;
    }
    return result;
}

function convert(){
    primary_cur = document.getElementById('byn_money');
    secondary_cur = document.getElementById('foreign_money');
    abbr = document.getElementById('choice').value;
    if (primary_cur.hasAttribute('required')) {
        secondary_cur.value = primary_cur.value * get_value(abbr);
    }
    else {
        primary_cur.value = secondary_cur.value / get_value(abbr);
    }
}

function swap_currencies() {
    primary_cur = document.getElementById('byn_money');
    secondary_cur = document.getElementById('foreign_money');
    if (primary_cur.hasAttribute('disabled')) {
        primary_cur.setAttribute('required',true);
        primary_cur.removeAttribute('disabled');
        secondary_cur.setAttribute('disabled', true);
        secondary_cur.removeAttribute('required');
    }
    else {
        primary_cur.setAttribute('disabled',true);
        primary_cur.removeAttribute('required');
        secondary_cur.setAttribute('true', true);
        secondary_cur.removeAttribute('disabled');
    }
}