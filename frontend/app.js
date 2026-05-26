async function checkURL(){
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("predictedURL");
    
    // if no url 
    if(!url)
        return;

    resultDiv.textContent = "Predicting..";
    
    const response = await fetch("https://malicious-url-detector-web-app.onrender.com", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url})
    });

    const data = await response.json();
    console.log("Model predicted: " + data.prediction); // "benign or malicious"
    return data;
}