fetch("https://api.github.com/users/rogala21")
    .then(response => response.json() )
    .then(coderData => console.log(coderData) )
    .catch(err => console.log(err)) 

async function fetchText() {
    input = document.getElementById("input").value;
    let response = await fetch("https://api.github.com/users/" + input);
    var coderData = await response.json();
    name_a_followers = coderData.name + " has " + coderData.followers + " followers";
    document.getElementById("name").innerHTML = name_a_followers;
    document.getElementById("profile_picture").src = coderData.avatar_url;
    return coderData
}