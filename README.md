# auto-scalers-energy-consumption

<h1 align="center">Autoscalers Energy Eonsumption</h1>


### Installation

1. Clone the repo:
   ````sh
   git clone https://github.com/AzimovS/auto-scalers-energy-consumption
   ```sh
   ````
2. Install the required dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```
3. Start a flask application:
   ```sh
   python main.py
   ```
4. Start locust:
   ```sh
   locust -f locust.py
   ```
   Indicate the number of users, rate, and host (http://127.0.0.1:5000/)
5. Start codecarbon:
   ```sh
   python record.py
   ```
   It will create (or append to existing one) emissions.csv file with your hardware electricity power consumption. Wait at least for 20 seconds before proceeding to the next step.
6. Start prediction:
   ```sh
   python ml.py
   ```
   It will create example.csv file with the predicted and actual values.

### Built With

- [Python](https://www.python.org/)
- [Locust](https://locust.io/)
- [RiverML](https://riverml.xyz/latest/)
- [CodeCarbon](https://github.com/mlco2/codecarbon)
