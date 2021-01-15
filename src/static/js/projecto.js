const repo = document.getElementById("repo")

function checkSubmit() {
    if (!repo.value.startsWith("https://github.com/")) {
        alert("La url de github tiene que empezar por \"https://github.com/\"")
        return false;
    }

    data = fetch()
    console.log(data)
    if (!repo.value.endsWith(".git")) {
        repo.value = repo.value + ".git"
    }
    return true;
}