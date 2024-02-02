async function copyToClipboard() {
    console.log("Copy button clicked");
    // Fetch the content of resp.txt from the Template directory
    const response = await fetch('/Template/responses.txt');
    const content = await response.text();

    // Check if the content is not empty
    if (content.trim() !== "") {
        // Create a temporary element (textarea) to hold the text
        var tempTextArea = document.createElement("textarea");
        tempTextArea.value = content;

        // Append the temporary element to the document
        document.body.appendChild(tempTextArea);

        // Select the text inside the temporary element
        tempTextArea.select();
        tempTextArea.setSelectionRange(0, 99999); // For mobile devices

        // Copy the selected text to the clipboard
        document.execCommand("copy");

        // Remove the temporary element from the document
        document.body.removeChild(tempTextArea);

        // You can add additional logic or feedback here, such as showing a tooltip or changing the button text
        alert("Text copied to clipboard!");
    } else {
        // If the file is empty, provide feedback to the user
        alert("File is empty. No content to copy!");
    }
}
