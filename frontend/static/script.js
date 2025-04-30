async function sendRequest() {
    const imageFile = document.getElementById("image-input").files[0];
    const prompt = document.getElementById("text-input").value;
    const model = document.querySelector('input[name="model"]:checked').value;
    console.log("MODEL:", model)

    if (!imageFile || !prompt) {
        alert("Please upload an image and enter a prompt.");
        return;
    }

    const formData = new FormData();
    formData.append("image", imageFile);
    formData.append("prompt", prompt);
    formData.append("model", model);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById("result-image").src = `data:image/png;base64,${data.image}`;
        } else {
            alert("Inference failed.");
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while processing your request.");
    }
}