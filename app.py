from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mobile_number = request.form.get("phoneNumber")

        try:
            mobile_number = phonenumbers.parse(mobile_number)
            if(phonenumbers.is_valid_number(mobile_number)):
                is_valid = "Valid Number"
            else:
                is_valid = "Invalid Number"
                is_possible = "Impossible Number"
                time_zones = "None"
                carrier_name = "None"
                region = "None"
                return render_template(
                    "result.html",
                    is_valid=is_valid,
                    is_possible=is_possible,
                    time_zones=time_zones,
                    carrier_name=carrier_name,
                    region=region,
                )
            # is_valid = phonenumbers.is_valid_number(mobile_number)
            if(phonenumbers.is_possible_number(mobile_number)):
                is_possible = "Possible Number"
            else:
                is_possible = "Impossible Number"
            # is_possible = phonenumbers.is_possible_number(mobile_number)
            time_zones = timezone.time_zones_for_number(mobile_number)
            carrier_name = carrier.name_for_number(mobile_number, "en")
            region = geocoder.description_for_number(mobile_number, "en")

            return render_template(
                "result.html",
                is_valid=is_valid,
                is_possible=is_possible,
                time_zones=time_zones,
                carrier_name=carrier_name,
                region=region,
            )
        except phonenumbers.phonenumberutil.NumberFormatException:
            return "Invalid Phone Number"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)