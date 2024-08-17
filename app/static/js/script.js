function predictSQL() {
    const sqlCommand = document.getElementById('sqlCommand').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `sql_command=${encodeURIComponent(sqlCommand)}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `<div class="alert alert-info">${data.result}</div>`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
}
