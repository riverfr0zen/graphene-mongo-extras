An example Flask app to demonstrate [graphene_mongo_extras](https://github.com/riverfr0zen/graphene-mongo-extras)

# Install and run the Flask app 

## poetry example

```
poetry install
export FLASK_APP=examples/example_flask_app.py
poetry shell
flask run
```

## Virtualenv example

```
virtualenv -p /usr/bin/python3 ./venv
source venv/bin/activate
pip install -r examples/requirements.txt
export FLASK_APP=examples/example_flask_app.py
flask run
```

Once the app is running, you should be able to go to `http://localhost:5000/graphql` and run the queries below. You can explore the available query operators through the graphiql Documentation Explorer.

# Example queries

```
{
    highscores(filtering: {
        filters: [
            {player_Icontains: "bo"}
        ]
      }) {
        edges{
            node {
                player
            }
        }
    }
}
```

```
{
    highscores(filtering: {
        op: "OR",
        filters: [
            {player_Icontains: "bo"},
            {player_Icontains: "j"}
        ]
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```

```
{
    highscores(filtering: {
        op: "OR",
        filters: [
              {
                  player_Icontains: "ji",
                  score_Gte: 10
              },
              {
                  player_Icontains: "je"
              },
        ]
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```

```
{
    highscores(filtering: {
        op: "OR",
        filters: [
            {score_Lt: 2},
            {player_Icontains: "zi"}
        ],
        filtersets: [
            {
                op: "AND",
                filters: [
                    {score_Gte: 10},
                    {player_Icontains: "je"}
                ]
            }
        ]
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```

Essentially the same logic as previous, just formed differently
```
{
    highscores(filtering: {
        op: "OR",
        filtersets: [
            {
                op: "OR",
                filters: [
                    {score_Lt: 2},
                    {player_Icontains: "zi"}
                ]
            },
            {
                op: "AND",
                filters: [
                    {score_Gte: 10},
                    {player_Icontains: "je"}
                ]
            }
        ]
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```

```
{
    highscores(filtering: {
        op: "AND",
        filtersets: [
            {
                op: "OR",
                filters: [
                    {player_Icontains: "bo"},
                    {player_Icontains: "j"}
                ]
            },
            {
                op: "OR",
                filters: [
                    {score_Lte: 1},
                    {score_Gte: 10},
                ]
            }
        ]
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```


## Embedded fields examples

```
{
    highscores(filtering: {
        filters: [
            {info_Continues_Lt: 1},
        ],
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```

```
{
    highscores(filtering: {
        op: "AND",
        filters: [
            {info_Difficulty_Icontains: "hard"},
            {info_Continues_Lt: 1},
        ],
    }) {
        edges{
            node {
                player
            }
        }
    }
}
```


## List of embedded fields examples

```
{
    games(filtering: {
        filters: [
            {options_Difficulty_Ne: "easy"}
        ]
      }) {
        edges{
            node {
                name
            }
        }
    }
}
```

```
{
    games(filtering: {
        op:"OR"
        filters: [
            {options_Difficulty_In: ["easy"]},
            {options_Continues_Gte: 40}
        ]
      }) {
        edges{
            node {
                name
            }
        }
    }
}
```
