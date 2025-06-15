async function updateCheckboxState(checkboxId) {
    const isChecked = document.getElementById(checkboxId).checked;
    const response = await fetch("http://localhost:5000/update_checkbox", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({checkbox_id: checkboxId, is_checked: isChecked})
    });
    const result = await response.json();
}