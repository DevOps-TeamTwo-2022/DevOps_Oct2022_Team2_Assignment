import pytest
from flaskPy import *
from flaskPy import app

#tests if server error occurred or redirection not done e.g redirect from / to /main automatically
def test_flaskPy_testOne():
  
  response = app.test_client().get('/')
  
  match_Open = app.test_client().get('/Match_Student')
  
  tempList = [str(response),str(match_Open)]
  
  print("Redirect to main",tempList[0],"Open Match_Student.html",tempList[1])
  
  errors = []

  if "500 internal" in tempList[0]:
    errors.append("Warning! 500 internal server error!")   
  if not "302 FOUND" in tempList[0]:
    errors.append("Warning! Redirection not found!")
  if "404 NOT FOUND" in tempList[1]:
    errors.append("Warning! 404 Not Found for Match_Student.html!")     

  assert not errors, "errors occured:\n{}".format("\n".join(errors))  
    
test_flaskPy_testOne()