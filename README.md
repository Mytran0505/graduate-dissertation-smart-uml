# graduate-dissertation-smart-uml
proposing methods to automatically design database and generate query statement from natural language description
# Flask PlantUML API
## Running the API
1. Run the Flask application: type `python app.py`
2. The API will be available at `http://127.0.0.1:5000/`.

## Testing with Postman
To send the request to your Flask API using Postman:
1. Open Postman.
2. Set Request Type: Ensure the request type is set to POST.
3. Set URL: Enter `http://127.0.0.1:5000/process-paragraph` in the URL field.
4. Set Headers:
* Click on the Headers tab.
* Add a header with the key "Content-Type" and value "application/json".
5. Set Body:
* Click on the Body tab.
* Select raw.
* Choose JSON from the dropdown menu.
* Enter the following JSON in the text area:
`{
    "paragraph": "Your input paragraph here"
}`

6. Send the Request: Click the `Send` button.


