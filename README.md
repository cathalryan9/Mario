# Mario
Finds the shortest path through a square grid containing obstacles. Mario can save the Princess!  
  
## How to use the API  
  
### Endpoints:  
  
POST /path:  
Returns an array of the shortest possible paths. Request must contain keys "size" and "grid".
If the grid is invalid it will return "error-flag": True.

Format example: {"size": 3, "grid": ['---m','---x','----','---p']}
  
GET /log:  
Returns all log entries of /path endpoint events of this session.  
  
  
## Web App  
  
Web app was implemented using Dash.  
App is served at [http://127.0.0.1:8050/dash](http://127.0.0.1:8050/dash/)