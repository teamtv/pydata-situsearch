# SituSearch

Sam Allardyce walks into the video analysis room.. “Morning, I was watching the last Arsenal match and there were a few situations I saw that I thought they would hurt us on Saturday. I want you to find me all of these situations from their last 5 games and find the times in our last 5 matches that we have faced similar situations. Let me have it this afternoon. Thanks” …….“Gaffer, that is going…” Big Sam slams the door “… to take hours… of work”.



### Installation

#### Clone the repository
To get started with this repository make sure you clone it using `git clone https://github.com/teamtv/pydata-situsearch.git`.

#### Install requirements
After making a local clone you it's preferred to create a virtual environment to keep you machine clean.

Then run:
```shell script
pip install -r requirements.txt
pip install -r requirements-local.txt
```

#### Getting tracking data
For this demo we use open tracking data provided by Metrica Sports. You can find more information about their datasets here: https://github.com/metrica-sports/sample-data

```shell script
cd data/raw
wget "https://github.com/metrica-sports/sample-data/blob/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv?raw=true" -O sample1_home.csv
wget "https://github.com/metrica-sports/sample-data/blob/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv?raw=true" -O sample1_away.csv
```


### Run it on your local machine
This project is able to run on your local machine without any additional dependencies like servers, daemons, brokers, etc.

#### Fill your local repository
You can fill your local repository using the command line tool. The tool will parse the Metrica files and write the serialized files on your local disk.
```shell script
cd src
python cmdline.py fill-local-repository
```

#### Select the right repository
Open `src/flask_api/__init__.py` and make sure you use the local repository.

#### Start the server
You can either use gunicorn or debug werkzeug server. To start the debug werkzeug server run:
```shell script
cd src
python run_app.py
```


## Diving in the code

Let's learn more about the code itself

### 1. Domain models
In favor of sharing knowledge about the domain between developers and domain experts, we create domain models. These models helps us to have a common language.

We try to use names that teach others about the domain. In the case of SituSearch we can identity three core tracking models:
1. [TrackingDataset](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L34)
2. [Frame](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L25)
3. [Point](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/tracking.py#L9)

For the search domain there are two models:
1. [ResultSet](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/search.py#L16)
2. [Result](https://github.com/teamtv/pydata-situsearch/blob/master/src/domain/models/search.py#L6)

### 2. Domain services
