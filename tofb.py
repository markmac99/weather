import facebook

def main():
  f = open("/tmp/tweet.txt", "r") 
  msg=f.read()
  f.close()
  
  #print(msg)
  
  graph = facebook.GraphAPI(access_token="EAAUP3nedtsoBAEIDNGWf0CJep9RGSdDNf5ZBEzhpPNTTt8RqJCffnmFdHBfOuqGHTkTZBM1X7wNRCITYhnpbTpDJB7ZAxvY5hfIpQfH8XrAhru4JrO2acs9xmvyi3wxl7PrNxa44ekK035CJw3njz1qoZBQ34jAZD")

  # Write 'Hello, world' to the active user's wall.
  graph.put_object(parent_object='me', connection_name='feed', message=msg)                                   

if __name__ == "__main__":
  main()
