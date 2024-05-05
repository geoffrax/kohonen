## Kohonen Challenge
Please see [kohonen.ipynb](kohonen.ipynb)

To get this thing working:
- Clone the repo.

### Running Code:
Run: 
- `docker build -t koho .`
- `docker run -p 5000:5000 koho`

Alternatively:
- `pip install -r requirements`
- `python ./kohonen.py`

Once the server is running, you can connect via:

- `http://localhost:5000/draw_map`
- `http://localhost:5000/draw_map?sizex=10&sizey=40`
- `http://localhost:5000/draw_map?inputs=20&sizex=10&sizey=40&iterations=100&learningrate=0.1`

Note: localhost, 127.0.0.1, 0.0.0.0 should all connect.

### Variables
Variables can be added in the address bar as above. Default variables / modifiers are:
- 'inputs', 20
- 'sizex', 10
- 'sizey', 10   
- 'iterations', 100
- 'learningrate', 0.1

### Outputs
The output of this kohonen app is a png image of a matplotlib graph of the kohonen graph.

### Notebook
The notebook contains an experimental space to run the code in a local environment - load it up and start modifying code.
