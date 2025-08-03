# Pioneer structure to flat playlist
Python snippet for recursively getting all the tracks from pioneer default fs to a single folder

## How to install
First make a venv
`python3 -m venv venv`

Activate venv
`source venv/bin/activate`

Install from requirements
`pip install -r requirements.txt`

## How to run

After activating the venv,
From CLI, put the "Pioneer/Contents" folder to squash as input and the desired output location as output

Run 
`python3 main.py {pioneer} {output}`

when you're done:
`deactivate`

## Troubleshooting

Please let us know any bugs as an issue on github
