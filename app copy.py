import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import schemas

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        data_request = request.form["data_request"]
        sample_data = request.form["sample_data"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(data_request, sample_data),
            temperature=0.6,
            max_tokens=2048
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text, data_request=data_request, sample_data=sample_data))

    result = request.args.get("result")
    data_request = request.args.get("data_request", "")
    sample_data = request.args.get("sample_data", "")
    print(result)
    return render_template("index.html", result=result, data_request=data_request, sample_data=sample_data)


def generate_prompt(data_request, sample_data):
    example = """Please recommend code to solve the following problem.
                 Please include comments and keep the code as simple as possible.

              Schemas:
              {schemas.Person}
              {schemas.Location}
              data sample;
                input id age gender $ city $ state $ height weight;
                datalines;
                1 35 Male New York NY 180 75
                2 28 Female Los Angeles CA 165 60
                3 42 Male San Francisco CA 175 80
                4 31 Female New York NY 160 55
                5 46 Male San Francisco CA 185 90
                ;
                run;

                data zipcodes;
                input city $ state $ zipcode $;
                datalines;
                New York NY 10001
                Los Angeles CA 90001
                San Francisco CA 94101
                ;
                run;
            
                Problem:
                How can I merge the sample data with the zipcodes data?

                Solution:
                data merged;
                    merge sample zipcodes;
                    by city state;
                run;
                """

    problem = example + "\n" + f"""Please recommend code to solve the following problem.
    
            Problem:
            {data_request}

            Solution:
            """

    sample_data_sections = sample_data.split('---')
    for i, section in enumerate(sample_data_sections):
        problem += f"\n\n---- Sample Data {i+1} ----\n{section}"
    
    return problem


if __name__ == '__main__':
    app.run(debug=True)