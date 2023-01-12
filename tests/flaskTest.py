import pytest 
from flaskPy import *
from flaskPy import app # Flask instance of the API

def flaskPy_testOne_redirection():
  
  response = app.test_client().get('/')
  
  #assert "302 FOUND" in response, "Redirection works!"
  
  passPassTest = []
  PassFailTest = []

  #if "302 FOUND" in response:
  #    testing.append("Redirection works!")
  if not "302 FOUND" in response:
      testing.append("Warning! Redirection Failed!")

  assert not testing, "Tests occured:\n{}".format("\n".join(testing))  
    
flaskPy_testOne_redirection()