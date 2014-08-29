Band
====

Band(CampMobile) API  Python version


ex)
  
  import json
  
  from Band import BandAPI
  
  band = BandAPI()
  
  jsonData = band.login(None,'+82101234567','password') or jsonData = band.login(email,None,'password')
  
  logindata = json.loads(jsonData ,encoding='utf-8')
  
  auth_token = loginData['result_data']['auth_token']
  
  user_id = loginData['result_data']['user_id']
  
  full_auth_token = band.createAuthToken(user_id,auth_token) //If remember, you can be used the next time.
  
  
  band.setAuthToken(full_auth_token)
  
  profile = band.getProfile() 
  
