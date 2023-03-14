import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from schemas import print_final_schemas

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        data_request = request.form["data_request"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_code(data_request),
            temperature=0.6,
            max_tokens=2048
        )
        return redirect(url_for("index", result=response.choices[0].text, data_request=data_request))

    result = request.args.get("result")
    data_request = request.args.get("data_request", "")
    return render_template("index.html", result=result, data_request=data_request)

def generate_code(data_request):
    example = f"""
            Please recommend code to solve the following problem.
            Assume you're an external client who is asking a data related question.
            You will get questions like "What is the total weight of people by zip code?"
            You need to write code to answer the question based off the "Schemas options" you see below.
            You can only use the tables and columns in the "Schemas options" to answer the question.
            Select the closest column names to the question. 
            Example: "What are the total number of positive cases"
            Selected Columns: "cases_positive_total"

            Schemas options:
            {print_final_schemas("schemas")}
            
            Example:
            What is the total weight of people by zip code?

            Table name: Person
            Columns:
            Person: {{'city': 'VARCHAR(255)', 'state': 'VARCHAR(255)', 'height': 'INT', 'weight': 'FLOAT'}}

            Table name: Location
            Columns:
            Location: {{'city': 'VARCHAR(255)', 'state': 'VARCHAR(255)', 'zipcode': 'VARCHAR(255)'}}

            Solution:
            data WeightByZipCode;
                merge Person (in=a) Location (in=b);
                by city state;
                if a and b;
                length zipcode $255;
                output;
            run;

            proc means data=WeightByZipCode sum;
                var weight;
                class zipcode;
            run;
            """

    problem = example + "\n" + f"""Please recommend code to solve the following problem.
    
            Problem:
            {data_request}

            Solution:
            """
    
    return problem


if __name__ == '__main__':
    app.run(debug=True)
