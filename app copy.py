import os

import openai
from flask import Flask, redirect, render_template, request, url_for

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
            max_tokens=1024
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)


def generate_prompt(data_request, sample_data):
    example = f"""data sample;
                input id age gender $ city $ state $ height weight;
                datalines;
                {sample_data}
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
                Create a data step that will merge these two datasets together.

                Solution:
                data sample_with_zip;
                    merge sample zipcodes;
                    by city state;
                run;"""
    
    problem = example + "\n" + f"""Please recommend code to solve the following problem.
    
            Problem:
            {data_request}

            Solution:
            """
    # print(problem)
    return problem

if __name__ == '__main__':
    app.run(debug=True)

    # tests:
    # 1. please give me the number of times each zipcode shows up in the dataset using proc sql
        # proc sql;
        #         select zipcode, count(*) as count
    # 2. please add another column for the bmi for each person in the dataset
    #         data sample_with_zip;
            #     merge sample zipcodes;
            #     by city state;
            #     bmi = weight / (height * height);
            # run;

# Sample data
# 1 35 Male New York NY 180 75
# 2 28 Female Los Angeles CA 165 60
# 3 42 Male San Francisco CA 175 80
# 4 31 Female New York NY 160 55
# 5 46 Male San Francisco CA 185 90