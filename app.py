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
            Here are table and column information. 
            Please write me SAS code to generate the following question:

            Schemas Options:
            {print_final_schemas("schemas")}

            Example:

            Schema Options:
            Table name: summary
            Columns:
            summary: {{'date': 'DATE', 'admin_level_1': 'VARCHAR(255)', 'state': 'VARCHAR(255)', 
            'tests_increase': 'INT', 'tests_total': 'INT',
            'deaths_total': 'INT', 'recovered_total': 'INT', 
            'hospitilzations_current': 'INT', 'hospitalizations_increase': 'INT', 
            'hospitalizations_total': 'INT', 'icu_current': 'INT', 'icu_total': 'INT'}}
            
            Question:
            What are the average hospitalizations in the last week?

            Solution:
            /* Set the date range for the last week */
            %let end_date = today(); /* Assuming today's date is the end date */
            %let start_date = intnx('day', &end_date, -6); /* Calculate the start date */

            /* Filter the data to include only the last week */
            data summary_last_week;
            set summary;
            where date between "&start_date"d and "&end_date"d;
            run;

            /* Calculate the average hospitalizations */
            proc means data=summary_last_week mean;
            var hospitilzations_current;
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
