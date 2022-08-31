date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
day = date.getDate();
document.getElementById("heading").innerHTML = "Steintest report - " + month + "/" + day + "/" + year;
